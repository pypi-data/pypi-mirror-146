from bait.bait import BaIt
import bait.bait_errors as BE
from obspy import read, UTCDateTime
import numpy as np


def miniproc(st):
    prs = st.copy()
    prs.detrend('demean')
    prs.detrend('simple')
    prs.taper(max_percentage=0.05, type='cosine')
    prs.filter("bandpass",
               freqmin=1,
               freqmax=30,
               corners=2,
               zerophase=True)
    return prs


BAIT_PAR_DICT = {
    'max_iter': 10,
    'opbk_main': {
          'tdownmax': 0.1,     # float: seconds depends on filtering
          'tupevent': 0.5,     # float: seconds depends on filtering
          'thr1': 6.0,         # float: sample for CF's value threshold
          'thr2': 10.0,        # float: sample for sigma updating threshold
          'preset_len': 0.6,   # float: seconds
          'p_dur': 1.0         # float: seconds
    },
    'opbk_aux': {
          'tdownmax': 0.1,
          'tupevent': 0.25,    # time [s] for CF to remain above threshold γ
          'thr1': 3,           # 10 orig
          'thr2': 6,           # 20 orig
          'preset_len': 0.1,   # sec
          'p_dur': 1.0         # sec
    },
    'test_pickvalidation': {
          'SignalAmp': [0.5, 0.05],
          'SignalSustain': [0.2, 5, 1.2],
          'LowFreqTrend': [0.2, 0.80]
    },
    'pickAIC': True,
    'pickAIC_conf': {
          'useraw': True,
          'wintrim_noise': 0.8,
          'wintrim_sign': 0.5
    }
}


BAIT_PAR_DICT_NEW = {
    'max_iter': 10,
    'opbk_main': {
          'tdownmax': 0.5167,     # float: seconds depends on filtering
          'tupevent': 1.0,     # float: seconds depends on filtering
          'thr1': 10.0,         # float: sample for CF's value threshold
          'thr2': 20.0,        # float: sample for sigma updating threshold
          'preset_len': 0.5,   # float: seconds
          'p_dur': 1.0         # float: seconds
    },
    'opbk_aux': {
          'tdownmax': 0.5167,
          'tupevent': 1.0,    # time [s] for CF to remain above threshold γ
          'thr1': 10,           # 10 orig
          'thr2': 20,           # 20 orig
          'preset_len': 0.15,   # sec
          'p_dur': 1.0         # sec
    },
    'test_pickvalidation': {
          'SignalAmp': [0.5, 0.01],
          'SignalSustain': [0.3, 5, 1.25, "MAX", 1],
          'LowFreqTrend': [0.5, 0.80]
    },
    'pickAIC': False,
    'pickAIC_conf': {
          'useraw': True,
          'wintrim_noise': 1.1,
          'wintrim_sign': 1.1
    }
}


# --------------------


straw = read("./tests_data/obspyread.mseed")
stproc = miniproc(straw)

straw_new = read("./tests_data/KP201710270109OGGMBAIT_PROC*.SAC")
stproc_new = read("./tests_data/KP201710270109OGGMBAIT_PROC*.SAC")


def test_setworktrace():
    """ Test the picker """
    errors = []
    BP = BaIt(stproc, stream_raw=straw, channel="*Z")
    BP._setworktrace("*Z", "PROC")
    pr = BP.wt
    BP._setworktrace("*Z", "RAW")
    ra = BP.wt
    #
    if np.array_equal(pr.data, ra.data):
        errors.append("Returned picks are equal, no difference")
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_raisingerror():
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    #
    BP.pickAIC = False
    BP.pickAIC_conf = {}
    #
    BP.CatchEmAll()

    # ========================================== Tests
    raised = False
    try:
        BP.extract_true_pick(idx=0, picker="AIC", compact_format=False)
    except BE.MissingAttribute:
        raised = True
    #
    if not raised:
        errors.append("AIC selection error not raised!")
    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all():
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    #
    BP.CatchEmAll()

    # ========================================== Tests

    picklist = BP.extract_true_pick(
                            idx="all", picker="AIC", compact_format=True)

    if len(picklist) != 2:
        errors.append("Wrong AIC list length returned")

    if not picklist[0][0] < picklist[1][0]:
        errors.append("Pick list AIC not sorted in UTCtime!")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 750000):
        errors.append("P1 AIC not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 710000):
        errors.append("P2 AIC not correct")

    # ------

    picklist = BP.extract_true_pick(
                            idx="all", picker="BK", compact_format=True)

    if len(picklist) != 2:
        errors.append("Wrong BK list length returned")

    if not picklist[0][0] < picklist[1][0]:
        errors.append("Pick list BK not sorted in UTCtime!")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("P1 BK not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 740000):
        errors.append("P2 BK not correct")

    # ------

    picklist = BP.extract_true_pick(
                            idx="all", picker="AIC", compact_format=False)

    if len(picklist) != 2:
        errors.append("Wrong ALL AIC pick list length returned")

    if not picklist[0][1]['iteration'] < picklist[1][1]['iteration']:
        errors.append("Iteration ALL AIC sorting not respected")

    # ------

    picklist = BP.extract_true_pick(
                            idx="all", picker="BK", compact_format=False)

    if len(picklist) != 2:
        errors.append("Wrong ALL BK pick list length returned")

    if not picklist[0][1]['iteration'] < picklist[1][1]['iteration']:
        errors.append("Iteration ALL BK sorting not respected")

    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_return_none():
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    # Modify to not pick anything ==> trick evaluation step
    BP.pick_test = {
          'SignalAmp': [0.1, 0.9]}
    #
    try:
        BP.CatchEmAll()
        # If I arrive here --> the exception is skipped (not good)
        errors.append("Exception skipped, false positive (TRUE pick found " +
                      "even though NO REAL TRUE pick are there!")
        assert not errors, "Errors occured:\n{}".format("\n".join(errors))
    except BE.MissingVariable:
        # BP.plotPicks(show=True)
        # ========================================== Tests
        picklist = BP.extract_true_pick(
                              idx="all", picker="AIC", compact_format=True)
        if picklist:
            errors.append("Something returned even though no TRUE pick found")

        pd = BP.extract_true_pick(
                              idx=0, picker="BK", compact_format=True)
        if pd:
            errors.append("Something returned even though no TRUE pick found")

        pd = BP.extract_true_pick(idx=0, picker="BK", compact_format=False)
        if pd:
            errors.append("Something returned even though no TRUE pick found")
        #
        assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all_new_1():
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    #
    BP.CatchEmAll()
    #
    # BP.plotPicks(show=True)
    # ========================================== Tests

    picklist = BP.extract_true_pick(idx="ALL",
                                    picker=["AIC", "BK"],
                                    compact_format=True)

    if len(picklist) != 2:
        errors.append("Wrong AIC list length returned")

    if not picklist[0][0] < picklist[1][0]:
        errors.append("Pick list AIC not sorted in UTCtime!")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 750000):
        errors.append("P1 AIC not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 740000):
        errors.append("P2 BK not correct")

    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all_new_2():
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    #
    BP.CatchEmAll()
    #
    # BP.plotPicks(show=True)
    # ========================================== Tests

    picklist = BP.extract_true_pick(idx="ALL",
                                    picker=["BK", "AIC", "BK"],
                                    compact_format=True)

    if len(picklist) != 2:
        errors.append("Wrong BK list length returned")

    if not picklist[0][0] < picklist[1][0]:
        errors.append("Pick list BK not sorted in UTCtime!")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("P1 BK not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 740000):
        errors.append("P2 BK not correct")

    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all_new_3():
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    #
    BP.CatchEmAll()
    #
    # BP.plotPicks(show=True)
    # ========================================== Tests

    picklist = BP.extract_true_pick(idx=0,
                                    picker="BK",
                                    compact_format=True)

    if len(picklist) != 1:
        errors.append("Wrong BK list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("P1 BK not correct")

    # ---
    picklist = BP.extract_true_pick(idx=0,
                                    picker="AIC",
                                    compact_format=True)

    if len(picklist) != 1:
        errors.append("Wrong AIC list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 750000):
        errors.append("P1 AIC not correct")

    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all_new_4():
    """ Testing the mixed query with list for the extraction """
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    #
    BP.CatchEmAll()
    #
    # BP.plotPicks(show=True)
    # ========================================== Tests

    picklist = BP.extract_true_pick(idx=[0, 1],
                                    picker=["BK", "AIC"],
                                    compact_format=True)

    if len(picklist) != 2:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("P1 BK not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 710000):
        errors.append("P2 AIC not correct")
    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all_new_5():
    """ Testing the mixed query with list for the extraction """
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    #
    BP.CatchEmAll()
    #
    # BP.plotPicks(show=True)
    # ========================================== Tests

    picklist = BP.extract_true_pick(idx=[0, 1, 3],
                                    picker=["BK", "AIC", "BK"],
                                    compact_format=True)

    if len(picklist) != 2:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("P1 BK not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 710000):
        errors.append("P2 AIC not correct")
    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all_new_6():
    """ Testing the mixed query with list for the extraction """
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)
    #
    BP.CatchEmAll()
    #
    # BP.plotPicks(show=True)
    # ========================================== Tests

    picklist = BP.extract_true_pick(idx=[0, 3],
                                    picker=["BK", "AIC"],
                                    compact_format=True)

    if len(picklist) != 1:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("P1 BK not correct")
    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all_new_7():
    """ Testing the returning of empty list """
    errors = []
    #
    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)

    # ========================================== Tests

    picklist = BP.extract_true_pick(idx=[0, 3],
                                    picker=["BK", "AIC"],
                                    compact_format=True)

    if not isinstance(picklist, list):
        errors.append("The returned object is not a list")

    if picklist:
        errors.append("The empty list is not seen as None (empty)")
    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_returnedpick_all_new_8():
    """Testing the picker list increase with 'all' option selected
       Forcing bait to pick at least 3 VALID picks.
    """
    errors = []
    #

    BAIT_PAR_DICT = {
        'max_iter': 10,
        'opbk_main': {
              'tdownmax': 0.1,     # float: seconds depends on filtering
              'tupevent': 0.5,     # float: seconds depends on filtering
              'thr1': 6.0,         # float: sample for CF's value threshold
              'thr2': 10.0,        # float: sample for sigma updating threshold
              'preset_len': 0.6,   # float: seconds
              'p_dur': 1.0         # float: seconds
        },
        'opbk_aux': {
              'tdownmax': 0.1,
              'tupevent': 0.2,    # time [s] for CF to remain above threshold γ
              'thr1': 1,           # 10 orig
              'thr2': 4,           # 20 orig
              'preset_len': 0.05,   # sec
              'p_dur': 1.0         # sec
        },
        'test_pickvalidation': {
              'SignalAmp': [0.5, 0.05],
              # 'SignalSustain': [0.2, 5, 1.2],
              # 'LowFreqTrend': [0.2, 0.80]
        },
        'pickAIC': True,
        'pickAIC_conf': {
              'useraw': True,
              'wintrim_noise': 0.8,
              'wintrim_sign': 0.5
        }
    }

    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)

    BP.CatchEmAll()
    # BP.plotPicks(show=False)
    # ========================================== Tests

    picklist = BP.extract_true_pick(idx='ALL',
                                    picker="AIC",
                                    compact_format=True)

    if len(picklist) != 4:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 750000):
        errors.append("P1 AIC not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("P2 AIC not correct")

    if picklist[2][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 710000):
        errors.append("P3 AIC not correct")

    if picklist[3][0] != UTCDateTime(2009, 8, 24, 0, 20, 9, 400000):
        errors.append("P4 AIC not correct")
    #

    picklist = BP.extract_true_pick(idx='ALL',
                                    picker="BK",
                                    compact_format=True)

    if len(picklist) != 4:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("P1 BK not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 950000):
        errors.append("P2 BK not correct")

    if picklist[2][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 770000):
        errors.append("P3 BK not correct")

    if picklist[3][0] != UTCDateTime(2009, 8, 24, 0, 20, 9, 600000):
        errors.append("P4 BK not correct")
    #

    picklist = BP.extract_true_pick(idx='ALL',
                                    picker=["AIC", "AIC"],
                                    compact_format=True)

    if len(picklist) != 4:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 750000):
        errors.append("Mixed P1 AIC not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("Mixed P2 AIC not correct")

    if picklist[2][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 770000):
        errors.append("Mixed P3 BK not correct")

    if picklist[3][0] != UTCDateTime(2009, 8, 24, 0, 20, 9, 600000):
        errors.append("Mixed P4 BK not correct")
    #

    picklist = BP.extract_true_pick(idx='ALL',
                                    picker=["BK", "BK"],
                                    compact_format=True)

    if len(picklist) != 4:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("Mixed P1 BK not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 950000):
        errors.append("Mixed P2 BK not correct")

    if picklist[2][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 770000):
        errors.append("Mixed P3 BK not correct")

    if picklist[3][0] != UTCDateTime(2009, 8, 24, 0, 20, 9, 600000):
        errors.append("Mixed P4 BK not correct")
    #

    picklist = BP.extract_true_pick(idx='ALL',
                                    picker=["BK", "AIC", "AIC", "bk"],
                                    compact_format=True)

    if len(picklist) != 4:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("Mixed P1 BK not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
        errors.append("Mixed P2 AIC not correct")

    if picklist[2][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 710000):
        errors.append("Mixed P3 AIC not correct")

    if picklist[3][0] != UTCDateTime(2009, 8, 24, 0, 20, 9, 600000):
        errors.append("Mixed P4 BK not correct")
    #

    picklist = BP.extract_true_pick(idx='ALL',
                                    picker=["AIC", "BK", "AIC", "bk"],
                                    compact_format=True)

    if len(picklist) != 4:
        errors.append("Wrong QUERY list length returned")

    if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 750000):
        errors.append("Mixed P1 AIC not correct")

    if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 950000):
        errors.append("Mixed P2 BK not correct")

    if picklist[2][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 710000):
        errors.append("Mixed P3 AIC not correct")

    if picklist[3][0] != UTCDateTime(2009, 8, 24, 0, 20, 9, 600000):
        errors.append("Mixed P4 BK not correct")
    #

    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_signalsutain_customtest():
    """Testing the picker list increase with 'all' option selected
       Forcing bait to pick at least 3 VALID picks.
    """
    errors = []
    #
    BAIT_PAR_DICT = {
        'max_iter': 10,
        'opbk_main': {
              'tdownmax': 0.1,     # float: seconds depends on filtering
              'tupevent': 0.5,     # float: seconds depends on filtering
              'thr1': 6.0,         # float: sample for CF's value threshold
              'thr2': 10.0,        # float: sample for sigma updating threshold
              'preset_len': 0.6,   # float: seconds
              'p_dur': 1.0         # float: seconds
        },
        'opbk_aux': {
              'tdownmax': 0.1,
              'tupevent': 0.2,    # time [s] for CF to remain above threshold γ
              'thr1': 1,           # 10 orig
              'thr2': 4,           # 20 orig
              'preset_len': 0.05,   # sec
              'p_dur': 1.0         # sec
        },
        'test_pickvalidation': {
              # 'SignalAmp': [0.5, 0.05],
              'SignalSustain': [0.2, 5, 1.2, 'MEAN'],
              # 'LowFreqTrend': [0.2, 0.80]
        },
        'pickAIC': True,
        'pickAIC_conf': {
              'useraw': True,
              'wintrim_noise': 0.8,
              'wintrim_sign': 0.5
        }
    }

    compare_mean_list_one = [14.212710256719546, 30.056322165377797,
                             25.506449689781277, 18.10447088170802,
                             10.5551024053402]
    compare_mean_list_four = [1.2973488006154745, 1.0131700919738775,
                              1.1227542329360998, 0.4774252395681936,
                              0.6372265971911042]
    #
    compare_max_list_one = [32.21091230926377, 69.82341667115651,
                            53.25440148722459, 41.34908947502605,
                            42.723350408468775]
    #
    compare_max_list_four = [2.411005376514236, 3.008350482705364,
                             2.693507151577753, 1.3388610274247856,
                             1.7949457361200214]

    BP = BaIt(stproc,
              stream_raw=straw,
              channel="*Z",
              **BAIT_PAR_DICT)

    BP.CatchEmAll()
    baitd = BP._getbaitdict()

    if not baitd['1']['evaluatePick_tests']['SignalSustain'][0]:
        errors.append("Signal Sustain [1] returned FALSE instead of TRUE")
    np.testing.assert_almost_equal(
        baitd['1']['evaluatePick_tests']['SignalSustain'][1],
        compare_mean_list_one, decimal=12)
    #
    if baitd['4']['evaluatePick_tests']['SignalSustain'][0]:
        errors.append("Signal Sustain [4] returned TRUE instead of FALSE")
    np.testing.assert_almost_equal(
        baitd['4']['evaluatePick_tests']['SignalSustain'][1],
        compare_mean_list_four, decimal=12)

    BP._setpicktestdict({'SignalSustain': [0.2, 5, 1.2, 'MAX']})
    BP.CatchEmAll()
    baitd = BP._getbaitdict()

    if not baitd['1']['evaluatePick_tests']['SignalSustain'][0]:
        errors.append("Signal Sustain [1] returned FALSE instead of TRUE")
    np.testing.assert_almost_equal(
        baitd['1']['evaluatePick_tests']['SignalSustain'][1],
        compare_max_list_one, decimal=12)
    #
    if not baitd['4']['evaluatePick_tests']['SignalSustain'][0]:
        errors.append("Signal Sustain [4] returned FALSE instead of TRUE")
    np.testing.assert_almost_equal(
                        baitd['4']['evaluatePick_tests']['SignalSustain'][1],
                        compare_max_list_four, decimal=12)
    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


def test_bait_wwrong_iteration_sorting():
    """ I.e max_it=10, pick dict order sorting is erroneous (1-10-2 ...)
        Fixed in v2.5.8
    """

    errors = []
    #
    BP = BaIt(stproc_new,
              stream_raw=straw_new,
              channel="*Z",
              **BAIT_PAR_DICT_NEW)
    #
    BP.pickAIC = False
    BP.pickAIC_conf = {}
    #
    BP.CatchEmAll()

    # ========================================== Tests
    tpl = BP.extract_true_pick(idx="all", picker="BK", compact_format=False)
    #
    if tpl[0][0] == "10" and tpl[1][0] == "5":
        errors.append("BAIT returns unsorted dict: i.e. iteration 10 prior 5!")
    if not tpl[0][0] == "5":
        errors.append("BAIT returns unsorted dict: first true must be 5th iter!")
    #
    assert not errors, "Errors occured:\n{}".format("\n".join(errors))


# ================= Picks (PRIOR *_new_8)
# =================

# # AIC
# if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 750000):
#     errors.append("P1 AIC not correct")

# if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 710000):
#     errors.append("P2 AIC not correct")

# # BK
# if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
#     errors.append("P1 BK not correct")

# if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 740000):
#     errors.append("P2 BK not correct")


# ================= Picks (AFTER *_new_8)
# =================

# # AIC
# if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 750000):
#     errors.append("P1 AIC not correct")

# if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
#     errors.append("P2 AIC not correct")

# if picklist[2][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 710000):
#     errors.append("P3 AIC not correct")

# if picklist[3][0] != UTCDateTime(2009, 8, 24, 0, 20, 9, 400000):
#     errors.append("P4 AIC not correct")

# [(UTCDateTime(2009, 8, 24, 0, 20, 7, 750000), 'IPD0'),
#  (UTCDateTime(2009, 8, 24, 0, 20, 7, 720000), 'EPD3'),
#  (UTCDateTime(2009, 8, 24, 0, 20, 8, 710000), 'EPU4'),
#  (UTCDateTime(2009, 8, 24, 0, 20, 9, 400000), 'EPU4')]

# # BK
# if picklist[0][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 720000):
#     errors.append("P1 BK not correct")

# if picklist[1][0] != UTCDateTime(2009, 8, 24, 0, 20, 7, 950000):
#     errors.append("P2 BK not correct")

# if picklist[2][0] != UTCDateTime(2009, 8, 24, 0, 20, 8, 770000):
#     errors.append("P3 BK not correct")

# if picklist[3][0] != UTCDateTime(2009, 8, 24, 0, 20, 9, 600000):
#     errors.append("P4 BK not correct")

# [(UTCDateTime(2009, 8, 24, 0, 20, 7, 720000), 'IPD0'),
#  (UTCDateTime(2009, 8, 24, 0, 20, 7, 950000), 'EPD3'),
#  (UTCDateTime(2009, 8, 24, 0, 20, 8, 770000), 'EPU4'),
#  (UTCDateTime(2009, 8, 24, 0, 20, 9, 600000), 'EPU4')]




#####################      IF NO PICKE-EVALUATION TEST, BAIT IS NOT
#####################      PICKING CORRECTLY...--> NO VALID PICKS
# def test_bait_no_eval():
#     """ I.e max_it=10, pick dict order sorting is erroneous (1-10-2 ...)
#         Fixed in v2.5.8
#     """

#     errors = []
#     #
#     BAIT_PAR_DICT_NEW['test_pickvalidation'] = None
#     BP = BaIt(stproc_new,
#               stream_raw=straw_new,
#               channel="*Z",
#               **BAIT_PAR_DICT_NEW)
#     #
#     BP.pickAIC = False
#     BP.pickAIC_conf = {}
#     #
#     BP.CatchEmAll()

#     # ========================================== Tests
#     tpl = BP.extract_true_pick(idx="all", picker="BK", compact_format=False)
#     #
#     if tpl[0][0] == "10" and tpl[1][0] == "5":
#         errors.append("BAIT returns unsorted dict: i.e. iteration 10 prior 5!")
#     if not tpl[0][0] == "5":
#         errors.append("BAIT returns unsorted dict: first true must be 5th iter!")
#     #
#     assert not errors, "Errors occured:\n{}".format("\n".join(errors))
