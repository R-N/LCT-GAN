from src.models.autoencoder import LatentTAE
from src.models.gan import LatentGAN
from src.models.architectures import FCGenerator, FCDiscriminator
from src.utils.evaluation import get_utility_metrics, stat_sim
from src.utils.ctabgan_synthesizer import Condvec

import pandas as pd
import numpy as np

import torch
from torch.autograd import Variable
Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

def latent_gan_experiment():

    bottleneck = 32
    gan_batch_size = 256
    gan_latent_dim = 100
    
    ae = LatentTAE(embedding_size=bottleneck)
    ae.fit(n_epochs=1)

    lat_data = ae.get_latent_dataset()
    lat_data_np = [ d.cpu().detach().numpy().flatten() for d in lat_data ]
    np.savetxt("./data/latent.csv", lat_data_np, delimiter=",")
    print(len(lat_data))

    gan = LatentGAN(bottleneck)
    latent_data = np.loadtxt("./data/latent.csv", delimiter=",")

    gan.fit(latent_data, ae.train_data, ae.transformer.output_info, epochs=10)

    cond_generator = Condvec(ae.train_data, ae.transformer.output_info)

    ### Generating a batch
    z = Tensor(np.random.normal(0, 1, (gan_batch_size, gan_latent_dim)))
    z_cond = Tensor(cond_generator.sample(gan_batch_size))
    z = torch.cat([z, z_cond], dim=1).to(gan.device)

    generated_rows = gan.generator(z)
    print(generated_rows)

    please_work = ae.decode(generated_rows, batch=True)
    print(please_work)


def ae_experiment():
    ae = LatentTAE()
    ae.fit()

    lat_data = ae.get_latent_dataset()
    # print(lat_data)
    lat_data_np = [ d.cpu().detach().numpy().flatten() for d in lat_data ]
    np.savetxt("./data/latent.csv", lat_data_np, delimiter=",")
    print(len(lat_data))

    reconstructed_data = ae.decode(lat_data)
    print(reconstructed_data)
    print(len(reconstructed_data))
    
    real_path = "./data/Adult.csv"
    fake_paths = ["./data/Adult_decoded.csv"]
    reconstructed_data.to_csv("./data/Adult_decoded.csv", index=False)

    print("Computing statistical similarities")

    adult_categorical = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'gender', 'native-country', 'income']

    # Storing and presenting the results as a dataframe
    stat_res_avg = []
    for fake_path in fake_paths:
        stat_res = stat_sim(real_path,fake_path,adult_categorical)
        stat_res_avg.append(stat_res)

    stat_columns = ["Average WD (Continuous Columns)","Average JSD (Categorical Columns)","Correlation Distance"]
    stat_results = pd.DataFrame(np.array(stat_res_avg).mean(axis=0).reshape(1,3),columns=stat_columns)
    print(stat_results)

    print("Computing Machine Learning performance")

    classifiers_list = ["lr","dt","rf","mlp"]

    # Storing and presenting the results as a dataframe
    result_mat = get_utility_metrics(real_path, fake_paths, "MinMax", test_ratio=0.20)
    result_df  = pd.DataFrame(result_mat,columns = ["Acc", "AUC", "F1_Score"])
    result_df.index = classifiers_list
    print(result_df)



if __name__ == "__main__":
    latent_gan_experiment()