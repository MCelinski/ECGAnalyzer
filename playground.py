# import wfdb 
# import pandas as pd
# from wfdb import processing
# record = wfdb.rdrecord('signals/mitdb/103', sampto=3000)
# annotation = wfdb.rdann('signals/mitdb/103', 'atr', sampto=3000)
# sig, fields = wfdb.rdsamp('signals/mitdb/103', channels=[0])

# wfdb.plot_wfdb(record=record, annotation=annotation, plot_sym=True,
#                    time_units='seconds', title='MIT-BIH Record 100',
#                    figsize=(10,4), ecg_grids='all')
# rrInterval = processing.calc_rr
# distanceRR = processing.ann2rr('signals/mitdb/103', 'atr', as_array=True)
# print(distanceRR)
# maxRR = distanceRR.max()
# minRR = distanceRR.min()
# meanhr = processing.calc_mean_hr(distanceRR, fs =fields['fs'], min_rr = minRR, max_rr = maxRR,rr_units = 'samples')
# print(meanhr)
# df = pd.DataFrame(fields,columns="Heart Rate",dtype=float)
# df.describe()

# sig, fields = wfdb.rdsamp('signals/mitdb/101', channels=[0])
# xqrs = processing.XQRS(sig=sig[:,0], fs=fields['fs'])
# xqrs.detect()

# wfdb.plot_items(signal=sig, ann_samp=[xqrs.qrs_inds])

