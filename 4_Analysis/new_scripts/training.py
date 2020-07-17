import torch.nn as nn
import numpy as np
import torch.optim as optim
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import seaborn as sns

from dataloaders import *
from autoencoder_networks import AutoEncoder

def one_epoch_train(train_dataloader, model):
    error = []
    tr_loss = 0
    number_samples = 0
    for idx, batch in enumerate(train_dataloader):
        x_1 = batch[0]
        x_1.to("cuda")
        optimizer.zero_grad()
        output = model(x_1)
        error = criterion(x_1, output)
        tr_loss += error.item()
        error.backward()
        optimizer.step()
        number_samples += batch[0].size(0)
    print(error.detach())
    return error/number_samples, model

def train_whole(number_epochs, train_dataloader, model):
    for epoch in range(number_epochs):
        error, model = one_epoch_train(train_dataloader, model)
        print("Finish epoch: {} with error".format(epoch, error))
    return error, model

def test_preds(model, test_dataloader):
    predictions = []
    real_values = []
    for idx, batch in enumerate(test_dataloader):
        x = batch[0]
        x.to("cuda")
        with torch.no_grad():
            output = model(x)
            predictions += list(output.cpu().numpy())
            real_values += list(x.cpu().numpy())
    return predictions, real_values

def evaluate():
    return 0

input_dimension = train.shape[1]
hidden_dimension = 2
number_epochs = 50
learning_rate = 0.0001


model = AutoEncoder(input_size=input_dimension, hidden_size=hidden_dimension)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), betas=(0.9, 0.99), lr=learning_rate)


errors, model = train_whole(number_epochs, train_dataloader, model)
predictions_validation, real_values_validation = test_preds(model, validation_dataloader)


predictions_test, real_values_test = test_preds(model, test_dataloader)

plt.subplot(121)
validation = np.power(np.array(predictions_validation) - np.array(real_values_validation), 2).mean(axis=1)
plt.hist(validation)
plt.title("VALIDATION")
plt.subplot(122)
test = np.power(np.array(predictions_test) - np.array(real_values_test), 2).mean(axis=1)
plt.hist(test)
plt.title("TEST")
# plt.plot(a)

plt.figure(3)
sns.heatmap(np.power(np.array(predictions_test) - np.array(real_values_test), 2).T)