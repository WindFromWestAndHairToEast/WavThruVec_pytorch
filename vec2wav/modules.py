import torch
import torch.nn as nn
from torch.nn.utils import spectral_norm

class ConditionalBatchNorm1d(nn.Module):
    
    """Conditional Batch Normalization"""

    def __init__(self, num_features, z_channels=128):
      super().__init__()

      self.num_features = num_features
      self.z_channels = z_channels
      self.batch_nrom = nn.BatchNorm1d(num_features, affine=False)

      self.layer = spectral_norm(nn.Linear(z_channels, num_features * 2))
      self.layer.weight.data.normal_(1, 0.02)  # Initialise scale at N(1, 0.02)
      self.layer.bias.data.zero_()             # Initialise bias at 0

    def forward(self, inputs, noise):
      # import pdb
      # pdb.set_trace()
      outputs = self.batch_nrom(inputs)
      gamma, beta = self.layer(noise).chunk(2, 1)
      gamma = gamma.view(-1, self.num_features, 1)
      beta = beta.view(-1, self.num_features, 1)

      outputs = gamma * outputs + beta

      return outputs
  
if __name__ == '__main__':
    # import pdb
    # pdb.set_trace()
    data=torch.randn(16, 1024,80)
    z = torch.randn(16, 128)
    cbn=ConditionalBatchNorm1d(1024)
    x=cbn(data,z)
    nn.Linear(192,64)
    print(x.shape)# 16,1024,80