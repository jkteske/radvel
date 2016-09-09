"""
Command Line Interface
"""
import os
from argparse import ArgumentParser
import imp
import warnings
import pickle

import radvel.driver

warnings.filterwarnings("ignore")
warnings.simplefilter('once', DeprecationWarning)

def main():
    psr = ArgumentParser(
        description="RadVel: The Radial Velocity Toolkit", prog='radvel'
    )

    subpsr = psr.add_subparsers(title="subcommands", dest='subcommand')

    # In the parent parser, we define arguments and options common to
    # all subcommands.
    psr_parent = ArgumentParser(add_help=False)
    psr_parent.add_argument(
        '-d', dest='outputdir', type=str,
        help="Working directory. Default is the same as the \
        configuration file (without .py)"
    )
    psr_parent.add_argument('-s','--setup',
        dest='setupfn', type=str, nargs='+', 
        help="Setup file[s]. Can chain multiple."
    )

    # Fitting    
    psr_fit = subpsr.add_parser(
        'fit', parents=[psr_parent],
        description="Perform max-likelihood fitting"
    )
    psr_fit.set_defaults(func=radvel.driver.fit)

    
    # Plotting
    psr_plot = subpsr.add_parser('plot', parents=[psr_parent],)
    psr_plot.add_argument('-t','--type',
        type=str, nargs='+',
        choices=['rv','corner','trend', 'derived'],
        help="type of plot(s) to generate"
    )
    psr_plot.add_argument(
        '--plotkw', dest='plotkw',action='store', default="{}", type=eval,
        help='''
        Dictionary of keywords sent to rv_multipanel_plot. 
        E.g. --plotkw "{'yscale_auto': True}"'
        ''',
    )
    
    psr_plot.set_defaults(func=radvel.driver.plots)

    
    # MCMC
    psr_mcmc = subpsr.add_parser(
        'mcmc', parents=[psr_parent],
        description="Perform MCMC exploration"
    )
    psr_mcmc.add_argument(
        '--nsteps', dest='nsteps', action='store',default=20000, type=float, 
        help='Number of steps per chain [20000]',)
    psr_mcmc.add_argument(
        '--nwalkers', dest='nwalkers', action='store', default=50, type=int,
        help='Number of walkers. [50]', 
    )
    psr_mcmc.set_defaults(func=radvel.driver.mcmc)


    # Derive hysical parameters
    psr_physical = subpsr.add_parser(
        'derive', parents=[psr_parent],
        description="Multiply MCMC chains by physical parameters. MCMC must"
        + "be run first"
    )

    psr_physical.set_defaults(func=radvel.driver.derive)
    
    # BIC 
    psr_bic = subpsr.add_parser('bic', parents=[psr_parent],)
    psr_bic.add_argument('-t',
        '--type', type=str, nargs='+', 
        choices=['nplanets'],
        help="type of BIC comparison to perform"
    )
    psr_bic.set_defaults(func=radvel.driver.bic)

    # Tables
    psr_table = subpsr.add_parser('table', parents=[psr_parent],)
    psr_table.add_argument('-t','--type',
        type=str, nargs='+',
        choices=['params','priors', 'nplanets'],
        help="type of plot(s) to generate"
    )
    psr_table.add_argument(
        '--header', action='store_true',
        help="included latex column header. Default just prints data rows"
    )
    
    psr_table.set_defaults(func=radvel.driver.tables)

    
    # Report
    psr_report = subpsr.add_parser(
        'report', parents=[psr_parent], 
        description="Merge output tables and plots into LaTeX report"
    )
    psr_report.add_argument(
        '--comptype', dest='comptype', action='store',
        default='nplanets', type=str, 
        help='Type of BIC model comparison table to include. \
Default: nplanets')

    psr_report.set_defaults(func=radvel.driver.report)


    # Default    
    #psr_def = subpsr.add_parser(
    #    'full', parents=[psr_parent],
    #    description="Perform max-likelihood fitting"
    #)
    #psr_def.set_defaults(func=radvel.driver.def)

    
    args = psr.parse_args()

    if args.outputdir is None:
        setupfile = args.setupfn[0]
        system_name = os.path.basename(setupfile).split('.')[0]
        outdir = os.path.join('./', system_name)
        args.outputdir = outdir
            
    if not os.path.isdir(args.outputdir):
        os.mkdir(outdir)
        
    args.func(args)


if __name__ == '__main__':
    main()