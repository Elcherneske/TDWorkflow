#!/usr/bin/env python
"""
Spectrum Summing Tool

This script performs spectrum summing on MS files using PyOpenMS.
It supports three summing methods: block summing, range summing, and precursor summing.

Usage:
    python spectrum_sum.py --input <input_file> --output-dir <output_dir> 
                          --method <block|range|precursor> [--block-size <size>] 
                          [--start-scan <scan>] [--end-scan <scan>] 
                          [--ms-level <level>] [--rt-tolerance <seconds>]
                          [--mz-tolerance <Da>]

Example:
    python spectrum_sum.py --input data.mzML --output-dir ./results --method block --block-size 5 --ms-level 1
"""

import os
import sys
import argparse
import numpy as np
import pyopenms

def parse_arguments():
    parser = argparse.ArgumentParser(description='Spectrum summing tool')
    parser.add_argument('--tool', required=True, choices=['openms', 'openmsutils'], 
                        help='Tool to use: openms or openmsutils')
    parser.add_argument('--input', required=True, help='Input MS file (.mzML, .mzXML)')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    parser.add_argument('--method', required=True, choices=['block', 'range', 'precursor'], 
                        help='Summing method: block, range, or precursor')
    parser.add_argument('--block-size', type=int, default=5, 
                        help='Number of spectra to sum in each block (for block method)')
    parser.add_argument('--start-scan', type=int, default=1, 
                        help='Start scan number (for range method)')
    parser.add_argument('--end-scan', type=int, default=100, 
                        help='End scan number (for range method)')
    parser.add_argument('--ms-level', type=int, choices=[1, 2], default=1, 
                        help='MS level (1 or 2)')
    parser.add_argument('--rt-tolerance', type=float, default=10.0, 
                        help='RT tolerance in seconds (for precursor method)')
    parser.add_argument('--mz-tolerance', type=float, default=0.001, 
                        help='m/z tolerance in Da (for precursor method)')
    
    return parser.parse_args()

def block_summing(exp, block_size, ms_level):
    """Sum spectra in blocks of specified size using PyOpenMS SpectraMerger"""
    print(f"Performing block summing with block size {block_size} for MS level {ms_level}")
    
    # Filter spectra by MS level
    filtered_exp = pyopenms.MSExperiment()
    for spec in exp:
        if spec.getMSLevel() == ms_level:
            filtered_exp.addSpectrum(spec)
    
    if filtered_exp.size() == 0:
        print(f"No spectra found with MS level {ms_level}")
        return filtered_exp
    
    print(f"Found {filtered_exp.size()} spectra with MS level {ms_level}")
    
    # Create a SpectraMerger object
    merger = pyopenms.SpectraMerger()
    
    # Set parameters for block merging
    params = merger.getParameters()
    params.setValue("block_method:rt_block_size", block_size)
    merger.setParameters(params)
    
    # Perform block-wise merging
    merger.mergeSpectraBlockWise(filtered_exp)
    
    print(f"Created {filtered_exp.size()} summed spectra")
    return filtered_exp

def range_summing(exp, start_scan, end_scan, ms_level):
    """Sum spectra in the specified scan range"""
    print(f"Performing range summing from scan {start_scan} to {end_scan} for MS level {ms_level}")
    
    # Filter spectra by scan number && ms level
    if start_scan > end_scan or start_scan < 1 or end_scan > exp.size() or end_scan < 1:
        print("Invalid scan range")
        return pyopenms.MSExperiment()
    
    filtered_spectra = []
    for scan_number, spectrum in enumerate(exp):
        if spectrum.getMSLevel() == ms_level and scan_number >= start_scan - 1 and scan_number <= end_scan:
            filtered_spectra.append(spectrum)
    
    if not filtered_spectra:
        print(f"No spectra found with MS level {ms_level} in the specified scan range")
        return pyopenms.MSExperiment()
    
    # Create a new experiment with only the selected range
    range_exp = pyopenms.MSExperiment()
    for spectrum in filtered_spectra:
        range_exp.addSpectrum(spectrum)
    
    block_size = range_exp.size()
    
    # Create a SpectraMerger object
    merger = pyopenms.SpectraMerger()
    
    # Set parameters for block merging
    params = merger.getParameters()
    params.setValue("block_method:rt_block_size", block_size)
    merger.setParameters(params)
    
    # Perform block-wise merging
    merger.mergeSpectraBlockWise(range_exp)
    
    print(f"Created {range_exp.size()} summed spectra")
    return range_exp

def precursor_summing(exp, ms_level, rt_tolerance, mz_tolerance):
    """Sum spectra with similar precursors (for MS2)"""
    if ms_level != 2:
        print("Precursor summing is only applicable for MS level 2")
        return pyopenms.MSExperiment()
    
    print(f"Performing precursor summing for MS level {ms_level}")
    
    # Filter spectra by MS level
    filtered_exp = pyopenms.MSExperiment()
    for spec in exp:
        if spec.getMSLevel() == ms_level:
            filtered_exp.addSpectrum(spec)
    
    if filtered_exp.size() == 0:
        print(f"No spectra found with MS level {ms_level}")
        return filtered_exp
    
    print(f"Found {filtered_exp.size()} spectra with MS level {ms_level}")
    
    # Create a SpectraMerger object
    merger = pyopenms.SpectraMerger()
    
    # Set parameters for precursor merging
    params = merger.getParameters()
    params.setValue("precursor_method:rt_tolerance", rt_tolerance)
    params.setValue("precursor_method:mz_tolerance", mz_tolerance)
    merger.setParameters(params)
    
    # Perform precursor-based merging
    merger.mergeSpectraPrecursors(filtered_exp)
    
    print(f"Created {filtered_exp.size()} summed spectra")
    return filtered_exp

def save_results(summed_exp, input_file, output_dir, method, params):
    """Save the summed spectra to output files"""
    if summed_exp.size() == 0:
        print("No summed spectra to save")
        return
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename
    input_basename = os.path.basename(input_file)
    input_name, _ = os.path.splitext(input_basename)
    
    if method == 'block':
        output_filename = f"{input_name}_block{params['block_size']}_MS{params['ms_level']}.mzML"
    elif method == 'range':
        output_filename = f"{input_name}_range{params['start_scan']}-{params['end_scan']}_MS{params['ms_level']}.mzML"
    else:  # precursor method
        output_filename = f"{input_name}_precursor_MS{params['ms_level']}.mzML"
    
    output_path = os.path.join(output_dir, output_filename)
    
    # Save the experiment to a file
    print(f"Saving summed spectra to {output_path}")
    pyopenms.MzMLFile().store(output_path, summed_exp)
    
    print(f"Saved {summed_exp.size()} summed spectra to {output_path}")
    return output_path

def main():
    args = parse_arguments()
    
    try:
        print(f"Loading MS file: {args.input}")
        exp = pyopenms.MSExperiment()
        pyopenms.MzMLFile().load(args.input, exp)
        print(f"Loaded {exp.size()} spectra")
        
        # Process spectra based on method
        if args.method == 'block':
            summed_exp = block_summing(exp, args.block_size, args.ms_level)
            params = {'block_size': args.block_size, 'ms_level': args.ms_level}
        elif args.method == 'range':
            summed_exp = range_summing(exp, args.start_scan, args.end_scan, args.ms_level)
            params = {'start_scan': args.start_scan, 'end_scan': args.end_scan, 'ms_level': args.ms_level}
        else:  # precursor method
            summed_exp = precursor_summing(exp, args.ms_level, args.rt_tolerance, args.mz_tolerance)
            params = {'ms_level': args.ms_level, 'rt_tolerance': args.rt_tolerance, 'mz_tolerance': args.mz_tolerance}
        
        # Save results
        output_path = save_results(summed_exp, args.input, args.output_dir, args.method, params)
        
        print("Processing completed successfully")
        return 0
    
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

