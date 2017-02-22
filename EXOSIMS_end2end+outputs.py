#! /usr/local/anaconda2/bin/python
##JX #! /usr/bin/env python 

import sys
sys.path.insert(0, '/home/jxie/EXOSIMS')
print(sys.path)
print 'in Python: sys.argv= ', sys.argv

import EXOSIMS.MissionSim as msim
import numpy as np
import pickle, json, os, csv
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import mosaic_tools as mt

import matplotlib  # JX
matplotlib.use('Agg')  # JX

# ===================================================================================================
#                            DEFINITIONS
# ===================================================================================================

def triple_axes_dist(ylog=False, xlog=False, topax=True, rightax=True,
                     figsize=(10, 10), xlabel='x', ylabel='y'):


    """Sets up plots with 3 axes -- one in center, one on right and one above center
    plot. The purpose is to have a scatter plot or w/e in the center, and two
    distribution plots of the x and y parameters in the side plots.
    Input:
    axScatter: axis object for center scatter plot
    ylog, xlog: booleans to indicate whether x and y axes of center plot are in
                log scale (base 10)
    xlabel, ylabel : labels for x and y axes labels

    Return
    """
    axScatter = plt.figure(111, figsize=figsize).add_subplot(111)
    axScatter.set_xlabel('%s' % xlabel, fontsize=25)
    axScatter.set_ylabel('%s' % ylabel, fontsize=25)

    divider = make_axes_locatable(axScatter)
    if topax:
        axHistX = divider.append_axes("top", size=2, pad=0.2, sharex=axScatter)
        plt.setp(axHistX.get_xticklabels(), visible=False)
    else:
        axHistX = None

    if rightax:
        axHistY = divider.append_axes("right", size=2, pad=0.2, sharey=axScatter)
        plt.setp(axHistY.get_yticklabels(), visible=False)
    else:
        axHistY = None

    if xlog:
        axScatter.set_xscale('log')
        axHistX.set_xscale('log', nonposy='clip')
    if ylog:
        axScatter.set_yscale('log')
        axHistY.set_yscale('log', nonposy='clip')

    return axScatter, axHistX, axHistY


def plot_setup(axis, gridon=False, minortickson=True,
               ticklabel_fontsize=20, majortick_width=2.5,
               minortick_width=1.2, majortick_size=8,
               minortick_size=5, axes_linewidth=1.5,
               ytick_direction='in', xtick_direction='in',
               yaxis_right=False, ylog=False, xlog=False):
    """Changes the boring default matplotlib plotting canvas so that it
    looks nice and neat with thicker borders and larger tick marks as well
    as larger fontsizes for the axis labels. Options exist to include or
    exclude the plot grid and minortick mark labels -- set up as boolean
    variables"""

    if gridon:
        axis.grid()
    if minortickson:
        axis.minorticks_on()
    if yaxis_right:
        axis.yaxis.tick_right()

    for line in axis.yaxis.get_majorticklines():
        line.set_markeredgewidth(majortick_width)
    for line in axis.xaxis.get_majorticklines():
        line.set_markeredgewidth(majortick_width)

    for line in axis.xaxis.get_minorticklines():
        line.set_markeredgewidth(minortick_width)
    for line in axis.yaxis.get_minorticklines():
        line.set_markeredgewidth(minortick_width)

    if xlog:
        axis.set_xscale('log', nonposy='clip')
    if ylog:
        axis.set_yscale('log', nonposy='clip')

    # plt.rc('text', usetex=True)
    plt.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})
    plt.rcParams['mathtext.fontset'] = 'stixsans'
    axis.tick_params(axis='both', which='major', labelsize=ticklabel_fontsize)
    plt.rc("axes", linewidth=axes_linewidth)
    plt.rcParams['xtick.major.size'] = majortick_size
    plt.rcParams['xtick.minor.size'] = minortick_size
    plt.rcParams['ytick.major.size'] = majortick_size
    plt.rcParams['ytick.minor.size'] = minortick_size

    plt.rcParams['xtick.direction'] = xtick_direction
    plt.rcParams['ytick.direction'] = ytick_direction

    plt.subplots_adjust(left=0.13, bottom=0.13, top=0.95, right=0.97)

    return


def linePlot(xdat, ydat, ax0=None, labels=('x', 'y'), xlog=False, ylog=False, **kw):
    """
    Input:
    ------
    xdat: numpy.array, x-axis data
    ydat: numpy.array, y-axis data
    ax0: None-type or axis object (plt.figure().add_subplot(111)). If None,
         an axis object is created.
    labels: 2x1 string-tuple, x and y-axis labels
    xlog, ylog: boolean, plot in log space.
    kw: dict, key-word dictionary of matplotlib plot inputs.

    Return:
    -------
    ax: axis plot object.
    """

    if ax0 is None:
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
    else:
        ax = ax0
    try:
        plot_setup(ax, ylog=ylog, xlog=xlog)
    except:
        print 'mosaic_tools not installed.'

    ax.plot(xdat, ydat, **kw)
    ax.set_xlabel(r'%s' % labels[0], fontsize=20)
    ax.set_ylabel(r'%s' % labels[1], fontsize=20)

    return ax


def scatterPlot(xdat, ydat, ax0=None, labels=('x', 'y'), xlog=False, ylog=False,
                figsize=(10, 10), **kw):
    """
    Input:
    ------
    xdat: numpy.array, x-axis data
    ydat: numpy.array, y-axis data
    ax0: None-type or axis object (plt.figure().add_subplot(111)). If None,
         an axis object is created.
    labels: 2x1 string-tuple, x and y-axis labels
    xlog, ylog: boolean, plot in log space.
    kw: dict, key-word dictionary of matplotlib plot inputs.

    Return:
    -------
    ax: axis plot object.
    """

    if ax0 is None:
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111)
    else:
        ax = ax0

    try:
        plot_setup(ax, ylog=ylog, xlog=xlog)
    except:
        print 'mosaic_tools not installed.'

    ax.plot(xdat, ydat, linestyle='None', **kw)
    ax.set_xlabel(r'%s' % labels[0], fontsize=20)
    ax.set_ylabel(r'%s' % labels[1], fontsize=20)

    return ax


def histPlot(xdat, bins=15, ax0=None, labels=('x', 'y'), xlog=False, ylog=False, **kw):
    """
    Input:
    ------
    xdat: numpy.array, x-axis data
    bins: int or numpy.array, bins.
    ax0: None-type or axis object (plt.figure().add_subplot(111)). If None,
         an axis object is created.
    labels: 2x1 string-tuple, x and y-axis labels
    xlog, ylog: boolean, plot in log space.
    kw: dict, key-word dictionary of matplotlib plot inputs.

    Return:
    -------
    ax: axis plot object.
    """

    if ax0 is None:
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
    else:
        ax = ax0

    try:
        plot_setup(ax, ylog=ylog, xlog=xlog)
    except:
        print 'mosaic_tools not installed.'

    ax.hist(xdat, bins, **kw)
    ax.set_xlabel(r'%s' % labels[0], fontsize=20)
    ax.set_ylabel(r'%s' % labels[1], fontsize=20)

    return ax


def reformat_DRM(drm):


    # list of keys to not do anything with -- in terms of expanding or concatenating.
    # THESE CAN BE UDPATED LATER
    dontdoanything = ['char_mode', 'slew_time', 'slew_angle', 'slew_dv', 'slew_mass_used',
                      'FA_fEZ', 'det_DV', 'det_mass_used', 'det_dF_lateral', 'det_dF_axial', 'char_dV',
                      'char_mass_used', 'char_dF_lateral', 'char_dF_axial', 'sc_mass']

    # list of keys whose array elements need to be repeated based on number of planets
    # detected per star.
    expand_keys = ['arrival_time', 'star_ind', 'det_time', 'char_time']

    # concatenate the arrays of these keys. In the end, each element in these arrays will have their
    # own individually mapped index in arrays in fill_keys.
    concatenate_keys = ['plan_inds', 'det_status', 'det_SNR', 'det_fEZ', 'det_dMag', 'det_WA',
                        'char_status', 'char_SNR', 'char_fEZ', 'char_dMag', 'char_WA',
                        'FA_status', 'FA_SNR', 'FA_dMag', 'FA_WA', ]

    # COLLECT ALL KEYS IN DRM AND UNIQUE-IFY THE ARRAY
    kys = np.array([dt.keys() for dt in drm])
    kys = np.unique(np.concatenate(kys))

    # CREATE DICTIONARY OF DRM BASED ON KEYWORDS
    ddrm = {}

    for ky in kys:

        # ADD VALUE, UNLESS EMPTY OR KEY DOE
        ddrm[ky] = np.array([[np.nan] if ky not in dt or
                             (not dt[ky] and not isinstance(dt[ky],(int,long,float)))
                             else dt.get(ky,[np.nan]) for dt in drm])

    plan_raw_inds = ddrm['plan_inds']

    # FILL OUT PROPER ARRAYS
    for ky in expand_keys:
        try:
            vals = ddrm[ky]
            # ADD SAME # AS PLANETS DETECTED.
            # AT LEAST ONE ADDED EVEN WITH NO PLANETS DETECTED
            temp_val = [[vals[i]] * len(plan_raw_inds[i])
                        for i in xrange(len(plan_raw_inds)) ]


            ddrm[ky] = np.concatenate(temp_val)
        except KeyError: print '%s not found.'%ky

    for ky in concatenate_keys:
        try:
            ddrm[ky] = np.concatenate(ddrm[ky])
        except KeyError: print '%s not found'%ky



    return ddrm


def varcsvOut(data):


    with open('Input_leftover_params.csv', 'wb') as myfile:
        w = csv.writer(myfile, delimiter=',')

        for key, val in data.items():

            if type(val) == list:
                i = 1
                # JX with open('./SimResults/Input_{}.csv'.format(key), 'wb') as myfile_list:
                with open('Input_{}.csv'.format(key), 'wb') as myfile_list:
                    wl = csv.writer(myfile_list)
                    for aitems in data[key]:
                        wl.writerow(['{}'.format(key), '{}'.format(i)])
                        for keyl, vall in aitems.items():
                            wl.writerow([keyl, vall])
                            myfile_list.flush()
                        i += 1

            elif type(val) == dict:
                with open('Input_{}.csv'.format(key), 'wb') as myfile_dict:
                    wd = csv.writer(myfile_dict)
                    for keyd, vald in data[key].items():
                        wd.writerow([keyd, vald])
                        myfile_dict.flush()

            else:
                w.writerow([key, val])
                myfile.flush()

def get_specs(jfile):
    script = open(jfile).read()
    specs = json.loads(script)
    return specs


def format_args(args):
    # KEEP ALL BUT FIRST ELEMENT OF ARGV.
    invar = np.array(args[1:])
    # REMOVES ALL DASHES
    invar2 = np.array([term.strip('-') for term in invar])
    invar3 = dict(np.resize(invar2, (invar2.size/2,2)))
    return invar3

# ==============================================================================
#      SKY PLOT OF ALL AND OBSERVED TARGETS
# ==============================================================================
def skyplot(ra, dec, figsize=(20, 20), projection='mollweide', axisbg='white',
            ticklcolor=None):

    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection=projection, axisbg=axisbg)

    plt.setp(ax.spines.values(), linewidth=10)
    if ticklcolor is not None:
        ax.set_xticklabels(tick_labels, color=ticklcolor)  # we add the scale on the x axis
    else:
        ax.set_xticklabels(tick_labels)

    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontweight('bold')
        tick.label1.set_fontsize(20)
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontweight('bold')
        tick.label1.set_fontsize(20)

    return ax

# ================================================================================

PT = mt.PlottingTools()


# ==============================================================================
#                     FOLDERS
# ==============================================================================
baseFolder = '/var/www/wfirst-dev/html/sims/tools/EXOSIMS-Testing/'
# JX resultFolder = os.path.join(baseFolder,'SimResults')
# JX resultFolder = os.path.join(baseFolder,'../results/')
resultFolder = os.path.join(baseFolder, '../')
scriptFolder = os.path.join(baseFolder, 'scripts')
compFolder = os.path.join(baseFolder, 'Completeness')
# ==============================================================================

# ==============================================================================
#                 INPUT VARIABLE DICTIONARY
# ==============================================================================
inputVars = format_args(sys.argv)

# ==============================================================================
#                   JSON INPUTS
# ==============================================================================


jfileBase = os.path.join(scriptFolder,'baseParams.json')
jfileObsMode = os.path.join(scriptFolder,'baseObservingModes.json')
jfileModules = os.path.join(scriptFolder,'baseModules.json')

modSpecs = get_specs(jfileModules)
obsSpecs = get_specs(jfileObsMode)
baseSpecs = get_specs(jfileBase)
useSpecs = baseSpecs.copy()


# THIS PIECE UPDATES THE INPUT VARIABLE FILE WITH INPUTS FROM THE USER INTERFACE
osmodekeys = ['lam','BW','SNR']


# REPLACE UNIVERAL PARAMS WITH INPUT VARS
for ikey, ivar in inputVars.iteritems():
    if ikey in useSpecs:
        try:
            useSpecs[ikey] = float(ivar)
        except ValueError: print '%s=%s cant be converted to float'%(ikey,ivar)
# REPLACE INPUT OF BAND INFO AND CREATE OBSERVING MODE ARRAY
for okey in osmodekeys:
    try:
        obsSpecs['HLC_Detection'][okey] = float(inputVars['D' + okey])
    except ValueError: print '%s=%s cant be converted to float'%(okey,inputVars['D' + okey])
    try:
        obsSpecs['SPC_Characterization'][okey] = float(inputVars['C' + okey])
    except ValueError: print '%s=%s cant be converted to float'%(okey,inputVars['D' + okey])

# CREATES LIST OF 2 OBSERVING MODES
useSpecs['observingModes'] = [obsSpecs['HLC_Detection'],
                              obsSpecs['SPC_Characterization']]

useSpecs['modules'] = modSpecs[inputVars['TargetType']]
# ==============================================================================

sim = msim.MissionSim(**useSpecs)  # RP
res = sim.SurveySimulation.run_sim()  # JX

# Stored detection information -- if any -- in DRM Dictionary
DRM = sim.SurveySimulation.DRM

# REFORMATTED DDRM
DDRM = reformat_DRM(DRM)

# Simulation specifications ; i.e., all parameters used in simulation
AllSpecs = sim.genOutSpec()
# =========================================================================================
#             OUTPUT CSV FILES
# =========================================================================================
varcsvOut(AllSpecs)
# =========================================================================================

TL = sim.TargetList
SC = sim.StarCatalog
SU = sim.SimulatedUniverse
SSim = sim.SurveySimulation
OS = sim.OpticalSystem
ZL = sim.ZodiacalLight
BS = sim.BackgroundSources
CP = sim.Completeness
PP = sim.PlanetPopulation
PM = sim.PlanetPhysicalModel

Name = TL.Name
Spec = TL.Spec
parx = TL.parx
Umag = TL.Umag
Bmag = TL.Bmag
Vmag = TL.Vmag
Rmag = TL.Rmag
Imag = TL.Imag
Jmag = TL.Jmag
Hmag = TL.Hmag
Kmag = TL.Kmag
dist = TL.dist
BV = TL.BV
MV = TL.MV
BC = TL.BC
L = TL.L
coords = TL.coords
pmra = TL.pmra
pmdec = TL.pmdec
rv = TL.rv
Binary_Cut = TL.Binary_Cut
# maxintTime = OS.maxintTime
comp0 = TL.comp0
MsEst = TL.MsEst
MsTrue = TL.MsTrue
nStars = TL.nStars

star_prop = {'Name': Name, 'Spec': Spec, 'parx': parx, 'Umag': Umag, 'Bmag': Bmag, 'Vmag': Vmag,
             'Imag': Imag, 'Jmag': Jmag, 'Hmag': Hmag, 'Kmag': Kmag, 'dist': dist, 'BV': BV,
             'MV': MV, 'Lum': L, 'coords': coords, 'pmra': pmra, 'pmdec': pmdec, 'rv': rv,
             'Binary_Cut': Binary_Cut, 'comp0': comp0, 'MsEst': MsEst,
             'MsTrue': MsTrue, 'nStars': nStars}  # ,'maxintTime':maxintTime}

try:
    arange = TL.arange
    erange = TL.erange
    wrange = TL.wrange
    Orange = TL.Orange
    prange = TL.prange
    Irange = TL.Irange
    Rrange, Mprange = TL.Rrange, TL.Mprange
    rrange = TL.rrange

except AttributeError:
    print 'Sorry.. no go.'
    print 'Not simulated planets.'

try:
    nPlans, plan2star = SU.nPlans, SU.plan2star
    sInds = SU.sInds
    # ORBTIAL PARAMETERS
    sma, ecc, wangle, Oangle, Iangle = SU.a, SU.e, SU.w, SU.O, SU.I
    # PLANET PROPERTIES
    Mp, Rp = SU.Mp, SU.Rp
    # POSITION AND VELOCITY VECTOR OF PLANET
    r, v = SU.r, SU.v
    # ALBEDO
    palbedo = SU.p
    fEZ = SU.fEZ


except AttributeError:
    print 'Sorry.. no go.'
    print 'Not ``real`` planets.'


# JX ------ end of Joan_EXOSIMS_end2end.py --- begin of Joan_EXOSIMS_outputs.py ------

# RP: COMMENTED THE NEXT LINE. 

Mprange = AllSpecs['Mprange']
arange = AllSpecs['arange']

# indices of targets observed in order including repeats
target_obsind = DDRM['star_ind']

# indices of all planets detected for each star.
try:
    detind_pl = DDRM['plan_inds']
# detind_pl = np.concatenate(detind_pl).astype('int32')
except:
    print 'No planets detected?'

# arrival time array
arrival_time = DDRM['arrival_time']

# angular distance of each detection ? mas
det_wa = DDRM['det_WA']

# status of any detections
det_status = DDRM['det_status']

# detection of planets
target_observed = Name[target_obsind]
detstatus_array = np.array([dt['det_status'] for dt in DRM])

# ===================================================================================================
#                 PLOTS
# ===================================================================================================


# SKY DISTRIBUTION OF TARGETS
save_plots = True  # JX False
plot_num = 1 # RP : PLOT NUMBER
# JX dirsave = os.path.join(baseFolder,'SimPlots')
# JX dirsave = os.path.join(baseFolder, '../results/')
dirsave = ''

ra = coords.ra.deg
ra[ra > 180] -= 360
ra = -1 * ra
ra_rad, dec_rad = np.radians(ra), coords.dec.radian
tick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
tick_labels = np.remainder(tick_labels + 360, 360)


axt = skyplot(ra_rad, dec_rad, axisbg='#E8E8E8')
try:
    plot_setup(axt)
except:
    pass
plt.grid(color='black', lw=2.5)
axt.plot(ra_rad, dec_rad, 'o', color='#00cc00', ms=10, mec='none', label='Stars in survey')
axt.plot(ra_rad[target_obsind], dec_rad[target_obsind], 'mo', ms=10, mec='m', mew=5)
txt = """RA vs. DEC OF ALL STARS IN THE SIMULATION (green) \n AND THOSE THAT WERE OBSERVED (red)"""
axt.set_title('%s' % txt, fontsize=30, y=1.03)
if save_plots:
    plot_num += 1
    plt.savefig(os.path.join(dirsave, 'fig%i.png' % plot_num), bbox_inches='tight')

# ================================================================================
#        OBSERVATION ORDER NUMBER
# ================================================================================
axt2 = skyplot(ra_rad, dec_rad, axisbg='#E8E8E8')
try:
    plot_setup(axt2)
except:
    pass
plt.grid(color='black', lw=2.5)
axt2.plot(ra_rad, dec_rad, 'o', color='#00cc00', ms=10, mec='none')
axt2.plot(ra_rad[target_obsind], dec_rad[target_obsind], 'mo', ms=10, mec='m', mew=5)

# axt2.plot(ra_rad[target_obsind],dec_rad[target_obsind],'r-',mew=2,lw=4,alpha=0.5)
axt2.tick_params(labelbottom='off', top='off', which='both', labelleft='off')
for i, j in enumerate(target_obsind):
    if i == 0:
        axt2.plot(ra_rad[j], dec_rad[j], 'm*', ms=26, mec='none')
    axt2.text(ra_rad[j], dec_rad[j], str(i + 1), color='k', fontsize=20)

txt = """RA vs. DEC OF ALL STARS IN THE SIMULATION (green) \n AND THOSE THAT WERE OBSERVED (red).
NUMBERS ARE ASSIGNED TO ORDER OF OBSERVATION."""
axt2.set_title('%s' % txt, fontsize=30, y=1.03)
if save_plots:
    plot_num += 1
    plt.savefig(os.path.join(dirsave, 'fig%i.png' % plot_num), bbox_inches='tight')
    plt.savefig(os.path.join(dirsave, 'fig%i.pdf' % plot_num), bbox_inches='tight')

# ================================================================================
#        OBSERVATION ORDER LINES
# ================================================================================
axt3 = skyplot(ra_rad, dec_rad, axisbg='#E8E8E8')
try:
    plot_setup(axt3)
except:
    pass
plt.grid(color='black', lw=2.5)
axt3.plot(ra_rad, dec_rad, 'o', color='#00cc00', ms=10, mec='none')

alp = np.logspace(-1, np.log10(0.6), len(target_obsind))  # [::-1]
for i in xrange(len(target_obsind)):
    if i == len(target_obsind) - 1:
        pass
    else:
        axt3.plot([ra_rad[target_obsind[i]], ra_rad[target_obsind[i + 1]]],
                  [dec_rad[target_obsind[i]], dec_rad[target_obsind[i + 1]]],
                  'm-', mew=2, lw=7, alpha=alp[i])

axt3.xaxis.label.set_color('lightgray')
axt3.tick_params(axis='both', colors='lightgray')

txt = """RA vs. DEC OF ALL STARS IN THE SIMULATION (green) \n AND THOSE THAT WERE OBSERVED (red).
ORDER OF OBSERVATIONS SHOWN BY TRACKS (light to dark)."""
axt3.set_title('%s' % txt, fontsize=30, y=1.03)

# plt.setp(axt2.spines.values(), color='lightgray',linewidth=10)
axt3.tick_params(labelbottom='off', top='off', which='both', labelleft='off')
for i, j in enumerate(target_obsind):
    if i == 0:
        axt3.plot(ra_rad[j], dec_rad[j], 'm*', ms=20, mec='none')
if save_plots:
    plot_num += 1
    plt.savefig(os.path.join(dirsave, 'fig%i.png' % plot_num), bbox_inches='tight')
    plt.savefig(os.path.join(dirsave, 'fig%i.pdf' % plot_num), bbox_inches='tight')

# ==================================================================================================================
#         CMD
# ==================================================================================================================
kw = {'markersize': 26, 'color': 'c', 'marker': 'o', 'alpha': .6, 'mec': 'none'}
axbv = scatterPlot(BV, MV, figsize=(15, 15), **kw)
axbv.plot(BV[target_obsind], MV[target_obsind], 'ro', markersize=16, mec='red', mew=2, alpha=0.7)
axbv.set_ylim(axbv.get_ylim()[::-1])
axbv.set_xlabel(r'B-V [mag]', fontsize=35)
axbv.set_ylabel(r'$M_V$ [mag]', fontsize=35)

txt = """COLOR-MAGNITUDE DIAGRAM OF ALL \nAND OBSERVED STARS IN SIMULATION."""
axbv.set_title('%s' % txt, fontsize=30, y=1.03)
if save_plots:
    plot_num += 1
    plt.savefig(os.path.join(dirsave, 'fig%i.png' % plot_num), bbox_inches='tight', edgecolor='none')
    plt.savefig(os.path.join(dirsave, 'fig%i.pdf' % plot_num), bbox_inches='tight', edgecolor='none')

# ==================================================================================================================
#            DISTANCE VS. B-V
# ==================================================================================================================

#kw = {'markersize': 6, 'color': 'g', 'marker': 'o', 'alpha': .6}
#axbvd = scatterPlot(dist, BV, labels=('Distance (pc)', 'B-V'), **kw)
# axbvd.plot(dist[target_obsind],BV[target_obsind],'ro',ms=6,mfc='none',mec='r',mew=2)
# axbvd.set_title('%s'%basesim)
# if save_plots: axbvd.savefig(os.path.join(dirsave,'target_dist_v_B-V_%s.png'%basesim))


# ********************************* Planet Plots ***************************
Rj = 69.911e6  # meters
Mj = 1.898e27  # Kg

# BINS & DATA
ebins = np.linspace(0, 1, 7)
logarange = np.log10(arange)
smabins = np.logspace(logarange[0], logarange[1], 10)
massbins = np.linspace(.001, 50, 20)

# =================================================================================
# HISTOGRAM OF PLANET MASS
binsl = np.logspace(-3, np.log10(50), 15)
axps = plt.figure(figsize=(15, 15)).add_subplot(111)
axps.hist(Mp / Mj, bins=binsl, histtype='step', lw=10, color='magenta', label='Generated Planets');
axps.hist(Mp[detind_pl] / Mj, bins=binsl, histtype='step', lw=10, color='green', alpha=0.7, label='Detected Planets');

axps.set_xlabel(r'Planet Mass [$M_J$]', fontsize=35)
axps.set_ylabel(r'Number of Stars', fontsize=35)

PT.simpleaxis1(axps)
plot_setup(axps, minortickson=False, majortick_size=15, majortick_width=5)
plt.setp(axps.spines.values(), linewidth=5)
axps.set_xlim(-2, (Mp.value / Mj).max() + 10)
axps.set_ylim(-1, 135)
axps.grid()

txt = """DISTRIBUTION OF PLANETS IN THE SURVEY"""
axps.set_title('%s' % txt, fontsize=30, y=1.03)

plt.minorticks_off()
plt.legend(loc='best', fontsize=20)
# if save_plots:
plot_num += 1
plt.savefig(os.path.join(dirsave, 'fig%i.png' % plot_num), bbox_inches='tight',edgecolor='none')
plt.savefig(os.path.join(dirsave, 'fig%i.pdf' % plot_num), bbox_inches='tight',edgecolor='none')

# =================================================================================


# MASS VS. RADIUS OF PLANETS
kw = {'markersize': 4, 'color': 'b', 'marker': 'o', 'alpha': .6}
axp = scatterPlot(Mp / Mj, Rp / Rj, labels=('Planet Mass ($M_J$)', 'Planet Radius ($R_J$)'),
                  xlog=True, ylog=True, **kw)
# JX if save_plots: axp.savefig(os.path.join(dirsave,'planet_R_v_M_%s.png'%basesim))


# HISTOGRAM OF SMA
kw = {'histtype': 'step', 'normed': True, 'lw': 3, 'color': 'g', 'label': 'Input Planets'}
axps = histPlot(sma, bins=smabins, labels=('SMA (AU)', 'Number of Stars'),
                xlog=True, **kw)
kw = {'histtype': 'step', 'normed': True, 'lw': 3, 'color': 'm', 'label': 'Detected Planets'}
axps = histPlot(sma[detind_pl], smabins, axps, labels=('SMA (AU)', 'Number of Stars'),
                xlog=True, **kw)
plt.legend()
# JX if save_plots: axps.savefig(os.path.join(dirsave,'planet_SMA_distribution_%s.png'%basesim))


# HISTOGRAM OF ECCENTRICITY
kw = {'histtype': 'step', 'lw': 3, 'color': 'g', 'label': 'Input Planets'}
axe = histPlot(ecc, bins=ebins, labels=('eccentricity', 'Number of Stars'), **kw)
axe.hist(ecc[detind_pl], bins=ebins, histtype='step', lw=3, color='m', label='Detected Planets');
plt.legend()
# JX if save_plots: axe.savefig(os.path.join(dirsave,'planet_ecc_distribution_%s.png'%basesim))

# HISTOGRAM OF PLANET MASS
kw = {'histtype': 'step', 'lw': 3, 'color': 'g', 'label': 'Input Planets'}
axmp = histPlot(Mp / Mj, bins=massbins,
                labels=(r'Planet Mass ($M_J$)', 'Number of Stars'), **kw)
axmp.hist(Mp[detind_pl] / Mj, bins=massbins, histtype='step', lw=3, color='magenta', label='Detected Planets')
plt.legend()
# JX if save_plots:axps.savefig(os.path.join(dirsave,'planet_SMA_distribution_%s.png'%basesim))


# CONTRAST CURVES
WA = DDRM['det_WA']
cntrst = 10 ** (DDRM['det_dMag'] / (-2.5))
kw = {'markersize': 26, 'color': 'r', 'marker': 'o', 'alpha': .6, 'mec': 'none'}
axcc = scatterPlot(WA, cntrst, figsize=(15, 15), **kw)
axcc.set_ylabel(r'Planet-Star Flux Ratio', fontsize=35)
axcc.set_xlabel(r'Working Angle (mas)', fontsize=35)
axcc.set_xlim(-20, WA.max() + 50)
plt.semilogy()

txt = """CONTRAST VS. WORKING ANGLE OF DETECTED PLANETS.\n IWA=0.0 mas, OWA=inf"""
axcc.set_title('%s' % txt, fontsize=30, y=1.03)
axcc.grid()
if save_plots:
    plot_num += 1
    plt.savefig(os.path.join(dirsave, 'fig%i.png' % plot_num), bbox_inches='tight',edgecolor='none')
    plt.savefig(os.path.join(dirsave, 'fig%i.pdf' % plot_num), bbox_inches='tight', edgecolor='none')

print 'All Done!'
