# ------------------------------------------------------------------------ #
# Copyright 2022 SPTK Working Group                                        #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License");          #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
# ------------------------------------------------------------------------ #

import warnings

import torch
import torch.nn as nn


class GeneralizedCepstrumGainNormalization(nn.Module):
    """See `this page <https://sp-nitech.github.io/sptk/latest/main/gnorm.html>`_
    for details.

    Parameters
    ----------
    cep_order : int >= 0 [scalar]
        Order of cepstrum, :math:`M`.

    gamma : float [-1 <= gamma <= 1]
        Gamma.

    c : int >= 1
        Inverse gamma.

    """

    def __init__(self, cep_order, gamma=0, c=None):
        super(GeneralizedCepstrumGainNormalization, self).__init__()

        self.cep_order = cep_order

        if c is None:
            self.gamma = gamma
        else:
            if gamma != 0:
                warnings.warn("gamma is given, but not used")
            self.gamma = 1 / c

        assert 0 <= self.cep_order
        assert abs(gamma) <= 1

    def forward(self, x):
        """Perform cepstrum gain normalization.

        Parameters
        ----------
        x : Tensor [shape=(..., M+1)]
            Generalized cepstrum

        Returns
        -------
        y : Tensor [shape=(..., M+1)]
            Normalized generalized cepstrum.

        Examples
        --------
        >>> x = diffsptk.ramp(1, 4)
        >>> gnorm = diffsptk.GeneralizedCepstrumGainNormalization(3, c=2)
        >>> y = gnorm(x)
        >>> y
        tensor([2.2500, 1.3333, 2.0000, 2.6667])

        """
        x0, x1 = torch.split(x, [1, self.cep_order], dim=-1)
        if self.gamma == 0:
            K = torch.exp(x0)
            y = x1
        else:
            z = 1 + self.gamma * x0
            K = torch.pow(z, 1 / self.gamma)
            y = x1 / z

        y = torch.cat((K, y), dim=-1)
        return y
