from torch import nn
import torch

class DNN(nn.Module):
    def __init__(self, dim_in):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(dim_in, 512),
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        logits = self.sigmoid(logits)
        return logits


def get_model(input_size, device):
    model = DNN(input_size).to(device)
    print(model)

    loss_fn = torch.nn.BCELoss(reduction="none")
    #loss_fn = torch.nn.CategoricalCrossEntropy(reduction="none")
    optimizer = torch.optim.Adam(model.parameters())

    return model, loss_fn, optimizer