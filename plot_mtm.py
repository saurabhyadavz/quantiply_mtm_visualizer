from __future__ import annotations
from common import *
import matplotlib.pyplot as plt

def plot_day_mtm(mtm_file: str=None):
    """Plot Day's MTM and save to current dir
        Args:
            mtm_file (str): MTM csv file
    """
    current_mtm_suff = f"mtm_{datetime.datetime.now().strftime('%d%m%Y')}"
    program_dir = os.getcwd() 
    mtm_filname = os.path.join(program_dir, f"{current_mtm_suff}.csv")
    if mtm_file:
      mtm_filname = mtm_file
    try:
      mtm_df = pd.read_csv(mtm_filname)
      mtm_df['pnl']=mtm_df['pnl'].astype(float)
      mtm_df.set_index('datetime', inplace=True)
      ax = mtm_df['pnl'].plot(kind='line', color='black')
      ax.fill_between(mtm_df.index, mtm_df['pnl'], where=mtm_df['pnl'] > 0, color='green')
      ax.fill_between(mtm_df.index, mtm_df['pnl'], where=mtm_df['pnl'] < 0, color='red')
      plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right', fontsize='x-small')
      plt.xlabel('datetime')
      plt.ylabel('pnl')
      plt.savefig(f'{current_mtm_suff}.png')
    except Exception as e:
      logging.error(f"An error occurred: {e}")

def parse_cmds() -> dict[str, typing.Any]:
    """Parses command line
        Returns:
            dict[str, typing.Any]: parsed arguments
    """
    parser = argparse.ArgumentParser(description="Plot days mtm from csv file"
                                     "having datetime and pnl as headers")
    parser.add_argument("-mtm_file", type=str, help="MTM csv file")
    return vars(parser.parse_args())

if __name__ == "__main__":
    args = parse_cmds()
    logging.basicConfig(level=logging.INFO)
    plot_day_mtm(args.get("mtm_file"))