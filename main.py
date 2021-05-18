import lightgbm as lgb
import pandas as pd
import datetime

# You should not modify this part.
def config():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="./sample_data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    return parser.parse_args()


def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


if __name__ == "__main__":
    args = config()

    df_gen = pd.read_csv(args.generation)
    df_con = pd.read_csv(args.consumption)
    gen = []
    con = []
    for i in range(len(df_gen)-144):
        gen.append([df_gen['generation'][i+24*0],
                    df_gen['generation'][i+24*1],
                    df_gen['generation'][i+24*2],
                    df_gen['generation'][i+24*3],
                    df_gen['generation'][i+24*4],
                    df_gen['generation'][i+24*5],
                    df_gen['generation'][i+24*6]])
        con.append([df_con['consumption'][i+24*0],
                    df_con['consumption'][i+24*1],
                    df_con['consumption'][i+24*2],
                    df_con['consumption'][i+24*3],
                    df_con['consumption'][i+24*4],
                    df_con['consumption'][i+24*5],
                    df_con['consumption'][i+24*6]])
        
    
    model_con = lgb.Booster(model_file='model_con.h5')
    model_gen = lgb.Booster(model_file='model_gen.h5')
    pred_gen = []
    pred_con = []
    for j in range(len(gen)):
        print(gen[j])
        pred_gen.append(model_gen.predict([gen[j]]))
        pred_con.append(model_con.predict([con[j]])) 
    print("pred")
    print(pred_gen)
    diff = []
    for j in range(len(gen)):
        diff.append(pred_gen[j][0] - pred_con[j][0])
    print(diff)
    last_time = list(df_gen['time'][-1:].str.split('-'))
    last_day = int(last_time[0][2].split(' ')[0])
    last_hour = int(last_time[0][2].split(' ')[1].split(':')[0])
    timestamp = datetime.datetime(int(last_time[0][0]), int(last_time[0][1]), last_day, last_hour)
    data = []
    for k in range(len(diff)):
        if diff[k] > 0:
            timestamp = timestamp + datetime.timedelta(hours=1)
            data.append([timestamp, 'sell', 1.5, diff[k]])
        else:
            timestamp = timestamp + datetime.timedelta(hours=1)
            data.append([timestamp, 'buy', 1.5, abs(diff[k])])
            
        
    
    output(args.output, data)
