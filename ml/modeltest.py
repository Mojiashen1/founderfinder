import torch
from torch.autograd import Variable
from torch.utils.data import Dataset, DataLoader

N, D_in, H, D_out = 1000, 50, 50, 1

x = Variable(torch.randn(N, D_in))
y = Variable(torch.randn(N, D_out), requires_grad=False)

model = torch.nn.Sequential(
          torch.nn.Linear(D_in, H),
          torch.nn.ReLU(),
          torch.nn.Linear(H, H),
          torch.nn.ReLU(),
          torch.nn.Linear(H, H),
          torch.nn.ReLU(),
          torch.nn.Linear(H, D_out),
        )

# loads saved model from file
# modelfile = Path("savedmodel.pt")
# if modelfile.is_file():
#     model = torch.load("savedmodel.pt")

loss_fn = torch.nn.MSELoss(size_average=False)

learning_rate = 1e-4
for t in range(500):
  y_pred = model(x)

  loss = loss_fn(y_pred, y)
  print(t, loss.data[0])
  
  model.zero_grad()
  loss.backward()

  # update the weights using gradient descent
  for param in model.parameters():
    param.data -= learning_rate * param.grad.data

torch.save(model, "savedmodel.pt")