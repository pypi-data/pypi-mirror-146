class Helper:

  @staticmethod
  def concatenate_metrics (metrics: list) -> str:
    return '\n'.join([ Helper.concatenate_metrics(metric) if type(metric) == list else str(metric) for metric in metrics ])
