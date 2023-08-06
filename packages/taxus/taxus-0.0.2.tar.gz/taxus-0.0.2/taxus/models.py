from gpytorch.models import ApproximateGP
from gpytorch.variational import (
    CholeskyVariationalDistribution,
    VariationalStrategy,
    UnwhitenedVariationalStrategy,
    IndependentMultitaskVariationalStrategy,
)
from gpytorch.priors import NormalPrior
from gpytorch.kernels import ScaleKernel, RBFKernel, Kernel, LinearKernel
from gpytorch.means import ConstantMean
from gpytorch.mlls import VariationalELBO
from gpytorch.distributions import MultivariateNormal
from patsy import dmatrix
import torch
from torch.optim import Adam
from tqdm import tqdm
import numpy as np
import pandas as pd
from typing import List

from .likelihoods import LIKELIHOODS


class GP(ApproximateGP):
    def __init__(
        self,
        formula: str,
        train_x_df: pd.DataFrame,
        train_y_df: pd.DataFrame,
        likelihood: str = 'nb',
        likelihood_kwargs: dict = dict(),
        kernel: str = 'rbf'
    ):
        train_x_df = dmatrix(f'{formula} -1', train_x_df,
                             return_type='dataframe')
        variational_strategy = self._get_variational_strategy(train_x_df)
        super(GP, self).__init__(variational_strategy)
        self.formula = formula
        self.train_y_df = train_y_df
        self.train_x_df = train_x_df

        _likelihood = LIKELIHOODS.get(likelihood)
        if not _likelihood:
            raise NameError(f'{likelihood} is not a valid likelihood name')
        self.likelihood = _likelihood(**likelihood_kwargs)
        self.mean_module = ConstantMean()
        self.covar_module = self._get_kernel_function(
            kernel, train_x_df.shape[1])
        self._kernel_name = kernel

    def _get_kernel_function(self, kernel_name: str, num_dims: int) -> Kernel:
        if kernel_name == 'rbf':
            return ScaleKernel(
                base_kernel=RBFKernel(
                    ard_num_dims=num_dims,
                    lengthscale_prior=NormalPrior(loc=0, scale=1)
                ),
                ard_num_dims=num_dims
            )
        elif kernel_name == 'linear':
            return ScaleKernel(
                base_kernel=LinearKernel(),
                ard_num_dims=num_dims
            )
        raise NameError(f'{kernel_name} is not a valid kernel name')

    def _get_variational_strategy(
        self, train_x_df: pd.DataFrame
    ) -> UnwhitenedVariationalStrategy:
        _inducing_points = torch.tensor(train_x_df.values, dtype=torch.float32)
        inducing_points = torch.unique(_inducing_points, dim=1)
        variational_distribution = CholeskyVariationalDistribution(
            num_inducing_points=inducing_points.size(0)
        )
        variational_strategy = UnwhitenedVariationalStrategy(
            self, inducing_points, variational_distribution,
            learn_inducing_locations=False
        )
        return variational_strategy

    @property
    def variable_names(self) -> List[str]:
        return list(self.train_x_df.columns)

    @property
    def train_y(self):
        return torch.tensor(self.train_y_df.values.T, dtype=torch.float32)

    @property
    def train_x(self):
        return torch.tensor(self.train_x_df.values, dtype=torch.float32)

    def forward(self, x: torch.tensor) -> MultivariateNormal:
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        latent_pred = MultivariateNormal(mean_x, covar_x)
        return latent_pred

    def fit(
        self,
        n_steps=600,
        lr=0.1,
        tol=1e-4,
        n_retries=2,
        show_progress_bar=True,
        debug=False
    ) -> float:
        """
        ELBO approximates (usually intractable) log marginal likelihood, \
        so can be used for likelihood ratio tests
        """
        self.losses_ = []
        mll = VariationalELBO(self.likelihood, self, self.train_y.size(1))

        optimizer = Adam([
            {'params': self.parameters()},
        ], lr=lr)

        self.train()
        self.likelihood.train()

        """
        if self._kernel_name == 'rbf':
            self.initialize(**{
                'covar_module.base_kernel.lengthscale': torch.tensor(
                    [2.]*self.train_x.shape[1]),
                'covar_module.outputscale': torch.log(self.train_y.mean()),
                'mean_module.constant': torch.log(self.train_y.mean())
            })
        else:
            self.initialize(**{
                'covar_module.outputscale': torch.log(self.train_y.mean()),
                'mean_module.constant': torch.log(self.train_y.mean())
            })
        """

        param_init = {
            'covar_module.outputscale': torch.log(self.train_y.mean()),
            'mean_module.constant': torch.log(self.train_y.mean())
        }

        if self._kernel_name == 'rbf':
            param_init['covar_module.base_kernel.lengthscale'] = torch.tensor(
                torch.max(torch.diff(self.train_x, axis=0), axis=0).values)

        self.initialize(**param_init)

        try:
            with tqdm(
                total=n_steps,
                desc='Fitting GP',
                leave=True,
                disable=not show_progress_bar,
            ) as progress_bar:
                for i in range(n_steps):
                    optimizer.zero_grad()
                    # Get predictive output
                    output = self(self.train_x)
                    # Calc loss and backprop gradients
                    loss = -mll(output, self.train_y)
                    loss_item = loss.item()
                    self.losses_.append(loss_item)
                    if i > 20 and abs(loss_item - self.losses_[-2]) < tol:
                        return loss_item
                    progress_bar.set_postfix(
                        loss=loss_item,
                    )
                    progress_bar.update()
                    loss.backward()
                    optimizer.step()
            return loss_item
        except Exception as e:
            if debug:
                print(e)
            if not n_retries:
                return np.nan
            self.fit(n_steps=n_steps, lr=lr, tol=tol, n_retries=n_retries-1,
                     show_progress_bar=show_progress_bar)

    def predict(
        self,
        test_x_df: pd.DataFrame,
        n_likelihood_samples=100,
        n_latent_samples=100,
        percentiles=[0.5, 2.5, 5, 50, 95, 97.5, 99.5]
    ) -> pd.DataFrame:
        test_x_df = (
            dmatrix(f'{self.formula} - 1', test_x_df, return_type='dataframe')
            # .drop('Intercept', axis=1, errors='ignore')
        )
        assert not (
            self.train_x_df.columns.difference(test_x_df.columns).values.size
        )
        test_x = torch.tensor(test_x_df.values, dtype=torch.float32)

        if (isinstance(self.likelihood, LIKELIHOODS['gaussian'])):
            # Gaussian likelihood has an exact implementation for marginal
            # probability so we don't have to sample, additionally setting this
            # higher than 1 results in incorrect number of total samples
            n_likelihood_samples = 1

        self.eval()
        self.likelihood.eval()

        f_pred = self(test_x)
        y_pred = self.likelihood(
            f_pred, sample_shape=torch.Size([n_likelihood_samples, 1])
        )

        model_samples = (
            y_pred.sample(torch.Size([n_latent_samples]))
            .reshape(n_latent_samples * n_likelihood_samples,
                     f_pred.mean.size(0))
            .numpy()
        )

        percentiles_pred = np.percentile(model_samples, percentiles, axis=0)

        return pd.DataFrame(
            np.concatenate([
                percentiles_pred.T,
                model_samples.mean(axis=0).reshape(-1, 1),
            ], axis=1),
            columns=[*[f'p{p}' for p in percentiles], 'mean']
        )

    def fit_predict(self, test_x_df: pd.DataFrame) -> pd.DataFrame:
        self.fit()
        return self.predict(test_x_df)


class MultiTaskGP(ApproximateGP):
    def __init__(self, train_x, n_outputs=1):
        inducing_points = torch.unique(train_x, dim=0)
        variational_distribution = CholeskyVariationalDistribution(
            num_inducing_points=inducing_points.size(0),
            batch_shape=torch.Size([n_outputs])
        )
        variational_strategy = IndependentMultitaskVariationalStrategy(
            VariationalStrategy(
                self, inducing_points, variational_distribution,
                learn_inducing_locations=False
            ),
            num_tasks=n_outputs,
            task_dim=-1
        )
        super(MultiTaskGP, self).__init__(variational_strategy)
        self.mean_module = ConstantMean(batch_shape=torch.Size([n_outputs]))
        self.covar_module = (
            ScaleKernel(
                RBFKernel(
                    ard_num_dims=3,
                    lengthscale_prior=NormalPrior(loc=0, scale=1),
                    batch_shape=torch.Size([n_outputs])
                ),
                batch_shape=torch.Size([n_outputs])
            )
            # ScaleKernel(RBFKernel(ard_num_dims=3))
            # ScaleKernel(MaternKernel(nu=0.5, ard_num_dims=3))
        )

    def forward(self, x):
        mean_x = self.mean_module(x)
        covar_x = self.covar_module(x)
        latent_pred = MultivariateNormal(mean_x, covar_x)
        return latent_pred
