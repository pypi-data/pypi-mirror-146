#!/usr/bin/env python3
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from typing import Dict

import torch
import torch.nn as nn
import torch.nn.functional as F

from .utils import register_grad_sampler


@register_grad_sampler(nn.GroupNorm)
def compute_group_norm_grad_sample(
    layer: nn.GroupNorm,
    activations: torch.Tensor,
    backprops: torch.Tensor,
) -> Dict[nn.Parameter, torch.Tensor]:
    """
    Computes per sample gradients for GroupNorm

    Args:
        layer: Layer
        activations: Activations
        backprops: Backpropagations
    """
    gs = F.group_norm(activations, layer.num_groups, eps=layer.eps) * backprops
    ret = {layer.weight: torch.einsum("ni...->ni", gs)}
    if layer.bias is not None:
        ret[layer.bias] = torch.einsum("ni...->ni", backprops)
    return ret
