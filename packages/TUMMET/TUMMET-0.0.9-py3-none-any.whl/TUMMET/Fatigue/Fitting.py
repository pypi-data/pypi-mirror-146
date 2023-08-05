import numpy as np
import pandas as pd
import os
from tkinter.filedialog import askdirectory, askopenfilenames
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

matplotlib.use('TkAgg')


def fit_ramberg_osgood(YoungsModulus, threshold=None, firstestimate=None, figurewidth='nature-singlecolumn',
                  figureheight=None, plotstyle='seaborn-deep', figurestyle='whitegrid', dpi=500, hue=True,
                  save=True, filetype='pdf', savedata=False):
    """Reads multiple evaluated excel files, calculates mean amplitudes, then fits Ramberg Osgood equation to the
    amplitudes and returns a fitting plot.

    Keyword arguments:
        YoungsModulus       -- YoungsModulus of the material. Float value in MPa.
        threshold           -- float between 0.0 and 1.0 depicting at what percentage of all Elapsed Cylcles
                               to start the stable zone. Beware of logic errors, when the end of the stable zone
                               falls before the start of the stable zone by using a too high threshold variable.
                               Will default to the previously determined stable zone if this error is encountered.
        firstestimate       -- List of values of K and n to use as a first estimate. Syntax [K, n]
        figurewidth         -- Width of figure. Float value in cm or one of the following:
                                    - 'nature-singlecolumn' --> Default
                                    - 'nature-oneandhalfcolumn'
                                    - 'nature-doublecolumn'
                                    - 'elsevier-minimal'
                                    - 'elsevier-singlecolumn'
                                    - 'elsevier-oneandhalfcolumn'
                                    - 'elsevier-doublecolumn'
                                    - 'science-singlecolumn'
                                    - 'science-doublecolumn'
                               Defaults to 'nature-singlecolumn'
        figureheight        -- Height of figure. Float value in cm. Defaults to value of figurewidth.
        plotstyle           -- Style of plot. One of the following:
                                    - 'seaborn-default' --> Default
                                    - 'seaborn-colorblind'
                                    - 'seaborn-rocket'
                                    - 'seaborn-crest'
                                    - 'seaborn-spectral'
                                    - 'red-blue'
        figurestyle         -- Seaborn figure Style. One of the following:
                                    - 'whitegrid' --> Default
                                    - 'white'
                                    - 'darkgrid'
                                    - 'dark'
                                    - 'ticks'

        dpi                 -- Dpi to save figure with. Int Value.
        hue                 -- True/False whether to uniquely identify the samples in the legend
        save                -- True/False whether to save the resulting figure.
        filetype            -- specify filetype as one of the following:
                                    - 'pdf' --> Default
                                    - 'png'
                                    - 'ps'
                                    - 'eps'
                                    - 'svg'
        savedata            -- True/False wheter to save the Dataframe as Excel file

        """
    figurewidths = {'nature-singlecolumn': 8.9,
                    'nature-oneandhalfcolumn': 12,
                    'nature-doublecolumn': 18.3,
                    'elsevier-minimal': 3,
                    'elsevier-singlecolumn': 9,
                    'elsevier-oneandhalfcolumn': 14,
                    'elsevier-doublecolumn': 19,
                    'science-singlecolumn': 5.5,
                    'science-doublecolumn': 12}
    plotstyles = {'seaborn-deep': 'deep',
                  'seaborn-colorblind': 'colorblind',
                  'seaborn-rocket': 'rocket',
                  'seaborn-crest': 'crest',
                  'seaborn-spectral': 'Spectral',
                  'red-blue': ['r']}
    if firstestimate is None:
        firstestimate = [600, 0.2]
    elif len(firstestimate) != 2:
        print('first estimation must be a list of length 2\n run "help(rambergosgood)" for details')
        return
    elif np.any(np.issubdtype(np.dtype(firstestimate), np.number)):
        print('first estimate must be numbers\n run "help(rambergosgood)" for details')
        return
    if figurestyle not in ['whitegrid', 'white', 'darkgrid', 'dark', 'ticks']:
        print('Figure style not in list\n run "help(rambergosgood)" for details')
        return
    sns.set_style(figurestyle)
    if filetype not in ['png', 'pdf', 'ps', 'eps', 'svg']:
        print('Filetype not in list\n run "help(rambergosgood)" for details')
        return

    if figurewidth not in ['nature-singlecolumn', 'nature-oneandhalfcolumn', 'nature-doublecolumn', 'elsevier-minimal',
                           'elsevier-singlecolumn', 'elsevier-oneandhalfcolumn', 'elsevier-doublecolumn',
                           'science-singlecolumn',
                           'science-doublecolumn'] and not np.issubdtype(type(figurewidth), np.number):
        print('Figurewidth not in list\n run "help(rambergosgood)" for details')
        return
    elif figurewidth not in ['nature-singlecolumn', 'nature-oneandhalfcolumn', 'nature-doublecolumn',
                             'elsevier-minimal',
                             'elsevier-singlecolumn', 'elsevier-oneandhalfcolumn', 'elsevier-doublecolumn',
                             'science-singlecolumn',
                             'science-doublecolumn'] and np.issubdtype(type(figurewidth), np.number):
        width = figurewidth
    else:
        width = figurewidths[figurewidth]

    if figureheight is None:
        figsize = (width / 2.54, width / 2.54)
    else:
        figsize = (width / 2.54, figureheight / 2.54)

    sns.set_context('notebook')

    filepaths = askopenfilenames(filetypes=[("Excel Files", '*.xlsx')], title='Which files shall be evaluated?')
    savedirectory = askdirectory(title='Where to save the results?')

    stressamplitudes, strainamplitudes = np.zeros(len(filepaths)), np.zeros(len(filepaths))

    for index, file in enumerate(filepaths):
        Sample = pd.read_excel(file, engine='openpyxl')

        if threshold is not None:
            lower = int(np.ceil(np.multiply(threshold, Sample['Elapsed Cycles'].max())))
            higher = int(Sample.index[Sample['Stable'] == 'Stable'].tolist()[-1])
            strainamplitudes[index] = np.mean(Sample.iloc[lower:higher, :]['Strain Amplitude (%)'])
            stressamplitudes[index] = np.mean(Sample.iloc[lower:higher, :]['Stress Amplitude (MPa)'])
            if not np.isfinite(stressamplitudes[index]) \
                    or not np.isfinite(strainamplitudes[index]) \
                    or np.isclose(0, stressamplitudes[index]) \
                    or np.isclose(0, strainamplitudes[index]):
                print(f'Error encountered for: {os.path.splitext(os.path.basename(file))[0]}'
                      f'\nMean of stable stress or strain is 0, inf or NaN, because threshold > end of stable zone'
                      '\nDefault calculation method used.')
                strainamplitudes[index] = np.mean(Sample.loc[Sample['Stable'] == 'Stable']['Strain Amplitude (%)'])
                stressamplitudes[index] = np.mean(Sample.loc[Sample['Stable'] == 'Stable']['Stress Amplitude (MPa)'])

        else:
            strainamplitudes[index] = np.mean(Sample.loc[Sample['Stable'] == 'Stable']['Strain Amplitude (%)'])
            stressamplitudes[index] = np.mean(Sample.loc[Sample['Stable'] == 'Stable']['Stress Amplitude (MPa)'])

    Samples = [os.path.splitext(os.path.basename(file))[0][:-18] for file in filepaths]
    Data = pd.DataFrame({'Samples': Samples,
                         'Strain Amplitude [%]': strainamplitudes,
                         'Stress Amplitude [MPa]': stressamplitudes})

    def rambergosgoodfunction(stressamplitudes, K, n):
        return np.divide(stressamplitudes, YoungsModulus) + pow(np.divide(stressamplitudes, K), np.divide(1, n))

    c, cov = curve_fit(rambergosgoodfunction, stressamplitudes, strainamplitudes, maxfev=100000)

    stressplot = np.linspace(0, 1.05 * Data['Stress Amplitude [MPa]'].max(), 10000)
    strainplot = np.divide(stressplot, YoungsModulus) + pow(np.divide(stressplot, c[0]), np.divide(1, c[1]))

    colormap = sns.color_palette(plotstyles[plotstyle], n_colors=len(Data) + 1)
    if plotstyle == 'red-blue':
        hue = False
        del colormap[0]
    elif plotstyle in ['seaborn-deep', 'seaborn-colorblind']:
        del colormap[0]
    else:
        del colormap[0]

    plt.figure(figsize=figsize)
    if hue:
        sns.scatterplot(data=Data, x='Strain Amplitude [%]', y='Stress Amplitude [MPa]', hue='Samples',
                        palette=colormap)
        plt.plot(strainplot, stressplot, label=f'ramberg-osgood\nK = {c[0]:.2f}\nn = {c[1]:.2f}',
                 color='b')
    else:
        sns.scatterplot(data=Data, x='Strain Amplitude [%]', y='Stress Amplitude [MPa]', label='Samples',
                        color=colormap[0])
        plt.plot(strainplot, stressplot, label=f'ramberg-osgood\nK = {c[0]:.2f}\nn = {c[1]:.2f}',
                 color='b')

    plt.legend(loc='center right')
    plt.title('Ramberg-Osgood Curve Fit')
    plt.tight_layout()
    if save:
        plt.savefig(savedirectory + os.sep + 'Ramberg-Osgood-fit.' + filetype, dpi=dpi)
    if savedata:
        Data.to_excel(savedirectory + os.sep + 'Ramberg-Osgood_curve_fit.xlsx', index=False)
    plt.show()
