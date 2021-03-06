#!/usr/bin/env python

import sys                          # system module
from optparse import OptionParser   # used for parsing command line arguments
import radiaUtil                    # utility functions for rna editing
import logging
import os
import subprocess
import gzip


'''
'    RNA and DNA Integrated Analysis (RADIA) identifies RNA and DNA variants in NGS data.
'    Copyright (C) 2010-2018  Amie Radenbaugh
'
'    This program is free software: you can redistribute it and/or modify
'    it under the terms of the GNU Affero General Public License as
'    published by the Free Software Foundation, either version 3 of the
'    License, or (at your option) any later version.
'
'    This program is distributed in the hope that it will be useful,
'    but WITHOUT ANY WARRANTY; without even the implied warranty of
'    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
'    GNU Affero General Public License for more details.
'
'    You should have received a copy of the GNU Affero General Public License
'    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


def get_read_fileHandler(aFilename):
    '''
    ' Open aFilename for reading and return
    ' the file handler.  The file can be 
    ' gzipped or not.
    '''
    if aFilename.endswith('.gz'):
        return gzip.open(aFilename,'rb')
    else:
        return open(aFilename,'r')


def get_write_fileHandler(aFilename):
    '''
    ' Open aFilename for writing and return
    ' the file handler.  The file can be 
    ' gzipped or not.
    '''
    if aFilename.endswith('.gz'):
        return gzip.open(aFilename,'wb')
    else:
        return open(aFilename,'w')


def filter_blacklist(aPythonExecutable, anId, aChromId, anInputFilename, anOutputDir, aPrefix, aBlacklistDir, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):

    filterFilename = os.path.join(aBlacklistDir, "chr" + aChromId + ".bed.gz")
    if (not os.path.isfile(filterFilename)):
        filterFilename = os.path.join(aBlacklistDir, "chr" + aChromId + ".bed")

    if (aGzipFlag):        
        outputFilename = os.path.join(anOutputDir, aPrefix + "_blacklist_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_blacklist_chr" + aChromId + ".vcf")

    script = os.path.join(aScriptsDir, "filterByPybed.py")        
    command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + filterFilename + " " + anInputFilename + " blck --includeFilterName -f \"##FILTER=<ID=blck,Description=\\\"Position overlaps 1000 Genomes Project blacklist\\\">\" -o " + outputFilename
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("FilterFilename: %s", filterFilename)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, filterFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def flag_dbSnp(aPythonExecutable, anId, aChromId, anInputFilename, anOutputDir, aPrefix, aDbSnpDir, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):
    
    filterFilename = os.path.join(aDbSnpDir, "chr" + aChromId + ".bed.gz")
    if (not os.path.isfile(filterFilename)):
        filterFilename = os.path.join(aDbSnpDir, "chr" + aChromId + ".bed")
        
    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_dbsnp_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_dbsnp_chr" + aChromId + ".vcf")
    
    script = os.path.join(aScriptsDir, "filterByCoordinate.py")
    
    command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + filterFilename + " " + anInputFilename + " DB --includeOverlaps --includeFilterName --includeIdName -d INFO -f \"##INFO=<ID=DB,Number=0,Type=Flag,Description=\\\"dbSNP common SNP membership\\\">\" -o " + outputFilename
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("FilterFilename: %s", filterFilename)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, filterFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def flag_retroGenes(aPythonExecutable, anId, aChromId, anInputFilename, anOutputDir, aPrefix, aRetroGeneDir, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):

    filterFilename = os.path.join(aRetroGeneDir, "chr" + aChromId + ".bed.gz")
    if (not os.path.isfile(filterFilename)):
        filterFilename = os.path.join(aRetroGeneDir, "chr" + aChromId + ".bed")
        
    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_retroGene_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_retroGene_chr" + aChromId + ".vcf")
    
    script = os.path.join(aScriptsDir, "filterByPybed.py")
    command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + filterFilename + " " + anInputFilename + " RTPS --includeOverlaps --includeFilterName -d INFO -f \"##INFO=<ID=RTPS,Number=0,Type=Flag,Description=\\\"Overlaps with retrotransposon or pseudogene\\\">\" -o " + outputFilename
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("FilterFilename: %s", filterFilename)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, filterFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)  
            sys.exit(1) 
            
    return outputFilename


def flag_pseudoGenes(aPythonExecutable, anId, aChromId, anInputFilename, anOutputDir, aPrefix, aPseudoGeneDir, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):

    filterFilename = os.path.join(aPseudoGeneDir, "chr" + aChromId + ".bed.gz")
    if (not os.path.isfile(filterFilename)):
        filterFilename = os.path.join(aPseudoGeneDir, "chr" + aChromId + ".bed")
    
    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_pseudoGene_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_pseudoGene_chr" + aChromId + ".vcf")
    
    script = os.path.join(aScriptsDir, "filterByPybed.py")
    command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + filterFilename + " " + anInputFilename + " EGPS --includeOverlaps --includeFilterName -d INFO -f \"##INFO=<ID=EGPS,Number=0,Type=Flag,Description=\\\"Overlaps with ENCODE/GENCODE pseudogenes\\\">\" -o " + outputFilename
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("FilterFilename: %s", filterFilename)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, filterFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def flag_cosmic(aPythonExecutable, anId, aChromId, anInputFilename, anOutputDir, aPrefix, aCosmicDir, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):

    filterFilename = os.path.join(aCosmicDir, "chr" + aChromId + ".bed.gz")
    if (not os.path.isfile(filterFilename)):
        filterFilename = os.path.join(aCosmicDir, "chr" + aChromId + ".bed")
    
    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_cosmic_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_cosmic_chr" + aChromId + ".vcf")
    
    script = os.path.join(aScriptsDir, "filterByPybed.py")
    command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + filterFilename + " " + anInputFilename + " COSMIC --includeOverlaps --includeFilterName -d INFO -f \"##INFO=<ID=COSMIC,Number=0,Type=Flag,Description=\\\"Overlaps with Catalogue Of Somatic Mutations In Cancer (COSMIC)\\\">\" -o " + outputFilename
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("FilterFilename: %s", filterFilename)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, filterFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def filter_targets(aPythonExecutable, anId, aChromId, anInputFilename, anOutputDir, aPrefix, aTargetDir, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):

    filterFilename = os.path.join(aTargetDir, "chr" + aChromId + ".bed.gz")
    if (not os.path.isfile(filterFilename)):
        filterFilename = os.path.join(aTargetDir, "chr" + aChromId + ".bed")
        
    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_targets_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_targets_chr" + aChromId + ".vcf")
    
    script = os.path.join(aScriptsDir, "filterByPybed.py")
    command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + filterFilename + " " + anInputFilename + " ntr --includeFilterName -f \"##FILTER=<ID=ntr,Description=\\\"Position does not overlap with a TCGA target region\\\">\" -o " + outputFilename
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("FilterFilename: %s", filterFilename)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, filterFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def filter_mpileupSupport_dna(aPythonExecutable, anId, aChromId, anInputFilename, aHeaderFilename, anOriginFlag, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):
  
    script = os.path.join(aScriptsDir, "filterByMpileupSupport.py")
    dnaParameterList = ["--genotypeMinPct=0.10", "--modMinDepth=4", "--modMinPct=0.10"]
    dnaParameterList += ["--dnaNormalMinTotalBases=10", "--dnaNormalMinAltBases=4", "--dnaNormalMinAltPct=0.10", "--dnaNormalMaxErrPct=0.01"]
    dnaParameterList += ["--dnaTumorMinTotalBases=10", "--dnaTumorMinAltBases=4", "--dnaTumorMinAltPct=0.10", "--dnaTumorMaxErrPct=0.01"]
    dnaParameterString = " ".join(dnaParameterList)
    if (anOriginFlag):
        if (aGzipFlag):
            outputFilename = os.path.join(anOutputDir, aPrefix + "_mpileup_dna_origin_chr" + aChromId + ".vcf.gz")
        else:
            outputFilename = os.path.join(anOutputDir, aPrefix + "_mpileup_dna_origin_chr" + aChromId + ".vcf")
            
        if (aHeaderFilename != None):
            command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + anInputFilename + " --addOrigin -o " + outputFilename + " -n " + aHeaderFilename + " " + dnaParameterString
        else:
            command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + anInputFilename + " --addOrigin -o " + outputFilename + " " + dnaParameterString
    else:
        if (aGzipFlag):
            outputFilename = os.path.join(anOutputDir, aPrefix + "_mpileup_dna_chr" + aChromId + ".vcf.gz")
        else:
            outputFilename = os.path.join(anOutputDir, aPrefix + "_mpileup_dna_chr" + aChromId + ".vcf")
            
        if (aHeaderFilename != None):
            command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + anInputFilename + " -o " + outputFilename + " -n " + aHeaderFilename + " " + dnaParameterString
        else:
            command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + anInputFilename + " -o " + outputFilename + " " + dnaParameterString
            
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def filter_mpileupSupport_rna(aPythonExecutable, anId, aChromId, anInputFilename, anOriginFlag, anRnaMinMapQual, anRnaMinAvgMapQual, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):
  
    script = os.path.join(aScriptsDir, "filterByMpileupSupport.py")
    rnaParameterList = ["--genotypeMinPct=0.0", "--modMinDepth=1", "--modMinPct=0.01"]
    rnaParameterList += ["--dnaNormalMinTotalBases=10", "--dnaNormalMinAltBases=0", "--dnaNormalMinAltPct=0.0", "--dnaNormalMaxErrPct=1.0", "--dnaNormalMinAltAvgBaseQual=15"]
    #rnaParameterList += ["--dnaNormalMinTotalBases=10", "--dnaNormalMinAltBases=0", "--dnaNormalMinAltPct=0.0", "--dnaNormalMaxErrPct=0.01", "--dnaNormalMinAltAvgBaseQual=15"]
    rnaParameterList += ["--dnaTumorMinTotalBases=1", "--dnaTumorMinAltBases=1", "--dnaTumorMinAltPct=0.01", "--dnaTumorMaxErrPct=1.0", "--dnaTumorMinAltAvgBaseQual=15"]
    #rnaParameterList += ["--dnaTumorMinTotalBases=1", "--dnaTumorMinAltBases=1", "--dnaTumorMinAltPct=0.01", "--dnaTumorMaxErrPct=0.01", "--dnaTumorMinAltAvgBaseQual=15"]
    rnaParameterList += ["--rnaNormalMinTotalBases=10", "--rnaNormalMinAltBases=4", "--rnaNormalMinAltPct=0.10", "--rnaNormalMaxErrPct=0.01", "--rnaNormalMinAltAvgBaseQual=15", "--rnaNormalMinAltMapQual=" + str(anRnaMinMapQual), "--rnaNormalMinAltAvgMapQual=" + str(anRnaMinAvgMapQual)]
    rnaParameterList += ["--rnaTumorMinTotalBases=10", "--rnaTumorMinAltBases=4", "--rnaTumorMinAltPct=0.10", "--rnaTumorMaxErrPct=0.01", "--rnaTumorMinAltAvgBaseQual=15", "--rnaTumorMinAltMapQual=" + str(anRnaMinMapQual), "--rnaTumorMinAltAvgMapQual=" + str(anRnaMinAvgMapQual)]

    rnaParameterString = " ".join(rnaParameterList)
    if (anOriginFlag):
        if (aGzipFlag):
            outputFilename = os.path.join(anOutputDir, aPrefix + "_mpileup_rna_origin_chr" + aChromId + ".vcf.gz")
        else:
            outputFilename = os.path.join(anOutputDir, aPrefix + "_mpileup_rna_origin_chr" + aChromId + ".vcf")
        command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + anInputFilename + " --addOrigin --filterUsingRNA -o " + outputFilename + " " + rnaParameterString
    else:
        if (aGzipFlag):
            outputFilename = os.path.join(anOutputDir, aPrefix + "_mpileup_rna_chr" + aChromId + ".vcf.gz")
        else:
            outputFilename = os.path.join(anOutputDir, aPrefix + "_mpileup_rna_chr" + aChromId + ".vcf")
        command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + anInputFilename + " --filterUsingRNA -o " + outputFilename + " " + rnaParameterString
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def radia_compare(aPythonExecutable, anId, aChromId, anRnaFilename, aDnaFilename, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):
    
    if (aGzipFlag):
        overlapFilename = os.path.join(anOutputDir, aPrefix + "_overlap_chr" + aChromId + ".vcf.gz")
    else:
        overlapFilename = os.path.join(anOutputDir, aPrefix + "_overlap_chr" + aChromId + ".vcf")
    
    if (aGzipFlag):
        nonOverlapFilename = os.path.join(anOutputDir, aPrefix + "_nonoverlap_chr" + aChromId + ".vcf.gz")
    else:
        nonOverlapFilename = os.path.join(anOutputDir, aPrefix + "_nonoverlap_chr" + aChromId + ".vcf")
    
    script = os.path.join(aScriptsDir, "radiaCompare.py")
    command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + anRnaFilename + " " + aDnaFilename + " -c \"SOM=SOM,NOR_EDIT=NOR_EDIT,TUM_EDIT=TUM_EDIT\" -o " + overlapFilename + " -n " + nonOverlapFilename 
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s %s", anRnaFilename, aDnaFilename)
        logging.debug("Output: %s %s", overlapFilename, nonOverlapFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anRnaFilename, aDnaFilename]
    writeFilenameList = [overlapFilename, nonOverlapFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return overlapFilename, nonOverlapFilename


def filter_rnaOnly(anId, aChromId, anInputFilename, anOutputDir, aPrefix, aJobListFileHandler, aGzipFlag, anIsDebug):

    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_dnaFiltered_chr" + aChromId + ".vcf.gz")
        #command = "zcat " + anInputFilename + " | grep -v \"dnm\" " + " | grep -v \"DB;\" | grep -v \"EGPS\" | grep -v \"RTPS\" | grep \"[SOM,EDIT]\" | gzip > " + outputFilename
        command = "zcat " + anInputFilename + " | grep -v \"dnm\" " + " | grep -v \"DB\" | grep -v \"EGPS\" | grep -v \"RTPS\" | grep \"[SOM,EDIT]\" | awk '{if ($1 ~ /^#/) {print} else {print $1\"\\t\"$2\"\\t\"$3\"\\t\"$4\"\\t\"$5\"\\t\"$6\"\\tPASS\\t\"$8\"\\t\"$9\"\\t\"$10\"\\t\"$11\"\\t\"$12}}' | gzip > " + outputFilename
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_dnaFiltered_chr" + aChromId + ".vcf")
        #command = "grep -v \"dnm\" " + anInputFilename + " | grep -v \"DB;\" | grep -v \"EGPS\" | grep -v \"RTPS\" | grep \"[SOM,EDIT]\" > " + outputFilename
        command = "grep -v \"dnm\" " + anInputFilename + " | grep -v \"DB\" | grep -v \"EGPS\" | grep -v \"RTPS\" | grep \"[SOM,EDIT]\" | awk '{if ($1 ~ /^#/) {print} else {print $1\"\\t\"$2\"\\t\"$3\"\\t\"$4\"\\t\"$5\"\\t\"$6\"\\tPASS\\t\"$8\"\\t\"$9\"\\t\"$10\"\\t\"$11\"\\t\"$12}}' > " + outputFilename
  
    if (anIsDebug):
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [anInputFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        
        # grep returns 0 if selected lines are found and 1 otherwise. But the exit status is 2 if an error occurred, 
        # unless the -q or --quiet or --silent option is used and a selected line is found. 
        
        
        #if (subprocessCall.returncode != 0):
        #    logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
        #    logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
                    
    return outputFilename


def extract_passing(anId, aChromId, anInputFilename, anOutputDir, aPrefix, aJobListFileHandler, aGzipFlag, anIsDebug):

    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_passing_chr" + aChromId + ".vcf.gz")
        command = "zcat " + anInputFilename + " | grep \"PASS\" " + " | gzip > " + outputFilename
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_passing_chr" + aChromId + ".vcf")
        command = "grep \"PASS\" " + anInputFilename + " > " + outputFilename
  
    if (anIsDebug):
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [anInputFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        
        # grep returns 0 if selected lines are found and 1 otherwise. But the exit status is 2 if an error occurred, 
        # unless the -q or --quiet or --silent option is used and a selected line is found. 
        
        
        #if (subprocessCall.returncode != 0):
        #    logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
        #    logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
                    
    return outputFilename


def filter_runSnpEff(anId, aChromId, anInputFilename, aSnpEffDir, aSnpEffGenome, aSnpEffCanonical, anOutputDir, aPrefix, aJobListFileHandler, anIsDebug):

    snpEffJar = os.path.join(aSnpEffDir, "snpEff.jar")
    snpEffConfig = os.path.join(aSnpEffDir, "snpEff.config")
    
    # by default, snpEff does not gzip the output
    # if we pipe the snpEff output to gzip, the return code and error messages from snpEff
    # get overwritten by gzip, and we no longer detect when there's a problem with snpEff
    outputFilename = os.path.join(anOutputDir, aPrefix + "_snpEff_chr" + aChromId + ".vcf")
    if (aSnpEffCanonical):
        command = "java -Xmx4g -jar " + snpEffJar + " eff -c " + snpEffConfig + " -canon -cancer -no-downstream -no-upstream -no-intergenic -no-intron " + aSnpEffGenome + " " + anInputFilename + " > " + outputFilename
    else:
        command = "java -Xmx4g -jar " + snpEffJar + " eff -c " + snpEffConfig + " -cancer -no-downstream -no-upstream -no-intergenic -no-intron " + aSnpEffGenome + " " + anInputFilename + " > " + outputFilename
            
    if (anIsDebug):
        logging.debug("Input: %s", anInputFilename)
        logging.debug("SnpEff: %s", snpEffJar)
        logging.debug("SnpEff: %s", snpEffConfig)
        logging.debug("SnpEff: %s", aSnpEffGenome)
        logging.debug("SnpEff: %s", aSnpEffCanonical)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [anInputFilename, snpEffJar, snpEffConfig]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)  
            sys.exit(1) 
                    
    return outputFilename


def filter_createBlatInput(aPythonExecutable, anId, aChromId, anInputFilename, aHeaderFilename, aTranscriptNameTag, aTranscriptCoordinateTag, aTranscriptStrandTag, anRnaIncludeSecondaryAlignmentsFlag, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, anIsDebug):

    # we can't gzip the blat input file
    outputFilename = os.path.join(anOutputDir, aPrefix + "_blatInput_chr" + aChromId + ".fa")
        
    script = os.path.join(aScriptsDir, "createBlatFile.py")
    
    if (aTranscriptNameTag != None and aTranscriptCoordinateTag != None):
        command = aPythonExecutable + " " + script + " " + anId + " " + anInputFilename + " " + aHeaderFilename + " -o " + outputFilename + " --allVCFCalls --blatRnaNormalReads --blatRnaTumorReads --transcriptNameTag " + aTranscriptNameTag + " --transcriptCoordinateTag " + aTranscriptCoordinateTag + " --transcriptStrandTag " + aTranscriptStrandTag
    else:
        command = aPythonExecutable + " " + script + " " + anId + " " + anInputFilename + " " + aHeaderFilename + " -o " + outputFilename + " --allVCFCalls --blatRnaNormalReads --blatRnaTumorReads"
    
    if (anRnaIncludeSecondaryAlignmentsFlag):
        command += " --rnaIncludeSecondaryAlignments"
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Header: %s", aHeaderFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, aHeaderFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
        
    return outputFilename


def filter_runBlat(anId, aChromId, aBlatInputFilename, aFastaFile, anOutputDir, aPrefix, aJobListFileHandler, anIsDebug):

    blatOutputFilename = anOutputDir + aPrefix + "_blatOutput_chr" + aChromId + ".blast"    
    #command = "blat -stepSize=5 -repMatch=2253 -minScore=0 -minIdentity=0 -t=dna -q=rna " + aFastaFile + " " + aBlatInputFilename + " -out=blast8 " + blatOutputFilename
    command = "blat -stepSize=5 -repMatch=2253 -t=dna -q=rna " + aFastaFile + " " + aBlatInputFilename + " -out=blast8 " + blatOutputFilename

    if (anIsDebug):
        logging.debug("Input: %s", aBlatInputFilename)
        logging.debug("Output: %s", blatOutputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [aBlatInputFilename, aFastaFile]
    writeFilenameList = [blatOutputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)  
            sys.exit(1)
            
    return blatOutputFilename


def filter_blat(aPythonExecutable, anId, aChromId, anInputFilename, aHeaderFilename, aBlatInputFilename, aFastaFile, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):
    
    # if no fasta file was specified, try to get it from the header file
    if (aFastaFile == None):
        fileHandler = get_read_fileHandler(aHeaderFilename)
         
        for line in fileHandler:
              
            # strip the carriage return and newline characters
            line = line.rstrip("\r\n")
            
            # if we find the vcfGenerator line, then create the dict of params
            if ("vcfGenerator" in line):
                generatorLine = line[0:(len(line)-1)]
                generatorLine = generatorLine[16:len(generatorLine)]
                generatorParamsList = generatorLine.split(",")
                generatorParamsDict = {}
                
                # create a dictionary of existing params
                for param in generatorParamsList:
                    (key, value) = param.split("=")
                    value = value.rstrip(">")
                    value = value.lstrip("<")
                    generatorParamsDict[key] = value
                
                break;
            
        fileHandler.close()
        
        if (("rnaTumorFastaFilename") in generatorParamsDict):
            aFastaFile = generatorParamsDict["rnaTumorFastaFilename"]
            
            if (not os.path.isfile(aFastaFile)):
                logging.critical("The FASTA file specified in the header does not exist: %s", aFastaFile, ". Specify a FASTA file for the RNA using the -f option.")
                sys.exit(1) 
        
    blatOutputFilename = filter_runBlat(anId, aChromId, aBlatInputFilename, aFastaFile, anOutputDir, aPrefix, aJobListFileHandler, anIsDebug)
        
    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_blatFiltered_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_blatFiltered_chr" + aChromId + ".vcf")
    
    script = os.path.join(aScriptsDir, "filterByBlat.py")
    command = aPythonExecutable + " " + script + " " + anId + " " + anInputFilename + " " + aBlatInputFilename + " " + blatOutputFilename + " -o " + outputFilename + " --allVCFCalls --blatRnaNormalReads --blatRnaTumorReads"
    
    if (anIsDebug):
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [anInputFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return (blatOutputFilename, outputFilename)


def filter_positionalBias(aPythonExecutable, anId, aChromId, anInputFilename, aBlatInputFilename, aKeepPreviousFiltersFlag, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):

    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_pbias_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_pbias_chr" + aChromId + ".vcf")
        
    script = os.path.join(aScriptsDir, "filterByPositionalBias.py")
    if (aKeepPreviousFiltersFlag):
        command = aPythonExecutable + " " + script + " " + anId + " " + anInputFilename + " " + aBlatInputFilename + " -o " + outputFilename + " --keepPreviousFilters"
    else:
        command = aPythonExecutable + " " + script + " " + anId + " " + anInputFilename + " " + aBlatInputFilename + " -o " + outputFilename
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Input: %s", aBlatInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, aBlatInputFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)  
            sys.exit(1) 
            
    return outputFilename


def filter_rnaBlacklist(aPythonExecutable, anId, aChromId, anInputFilename, aGeneBlckFilename, aGeneFamilyBlckFilename, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):

    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_rna_genes_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_rna_genes_chr" + aChromId + ".vcf")
        
    script = os.path.join(aScriptsDir, "filterByRnaBlacklist.py")
    command = aPythonExecutable + " " + script + " " + anInputFilename + " " + aGeneBlckFilename + " " + aGeneFamilyBlckFilename + " -o " + outputFilename
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Input: %s", aGeneBlckFilename)
        logging.debug("Input: %s", aGeneFamilyBlckFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename, aGeneBlckFilename, aGeneFamilyBlckFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)  
            sys.exit(1) 
            
    return outputFilename


def merge_rnaAndDna(aPythonExecutable, anId, aChromId, aDnaFilename, anRnaFilename, anOverlapsFilname, aNonoverlapsFilename, aDnaHeaderOnlyFlag, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):
  
    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_merged_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_merged_chr" + aChromId + ".vcf")
    
    script = os.path.join(aScriptsDir, "mergeRnaAndDnaFiles.py")
    if (aDnaHeaderOnlyFlag):
        command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + aDnaFilename + " " + anRnaFilename + " " + anOverlapsFilname + " " + aNonoverlapsFilename + " " + outputFilename + " --dnaHeaderOnly"
    else:
        command = aPythonExecutable + " " + script + " " + anId + " " + aChromId + " " + aDnaFilename + " " + anRnaFilename + " " + anOverlapsFilname + " " + aNonoverlapsFilename + " " + outputFilename
        
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s %s %s", aDnaFilename, anOverlapsFilname, aNonoverlapsFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, aDnaFilename, anOverlapsFilname]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def merge_passingAndOriginals(aPythonExecutable, anId, aChromId, aPassingCallsFilename, anOriginalFilname, anOutputDir, aPrefix, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):
  
    if (aGzipFlag):
        outputFilename = os.path.join(anOutputDir, aPrefix + "_mergedFinal_chr" + aChromId + ".vcf.gz")
    else:
        outputFilename = os.path.join(anOutputDir, aPrefix + "_mergedFinal_chr" + aChromId + ".vcf")
    script = os.path.join(aScriptsDir, "mergePassingAndOriginals.py")
    command = aPythonExecutable + " " + script + " " + aPassingCallsFilename + " " + anOriginalFilname + " " + outputFilename
        
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s %s", aPassingCallsFilename, anOriginalFilname)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, aPassingCallsFilename, anOriginalFilname]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            sys.exit(1)
            
    return outputFilename


def filter_readSupport(aPythonExecutable, anId, aChromId, anInputFilename, aTranscriptNameTag, aTranscriptCoordinateTag, aTranscriptStrandTag, anRnaIncludeSecondaryAlignmentsFlag, aMinMapQual, anOutputDir, aPrefix, anOutputFilename, aScriptsDir, aJobListFileHandler, aGzipFlag, anIsDebug):

    script = os.path.join(aScriptsDir, "filterByReadSupport.py")
    
    if (anOutputFilename != None):
        outputFilename = anOutputFilename
    else:
        if (aGzipFlag):
            outputFilename = os.path.join(anOutputDir, aPrefix + "_chr" + aChromId + ".vcf.gz")
            #command = aPythonExecutable + " " + script + " " + anInputFilename + " | gzip > " + outputFilename
        else:
            outputFilename = os.path.join(anOutputDir, aPrefix + "_chr" + aChromId + ".vcf")
            #command = aPythonExecutable + " " + script + " " + anInputFilename + " > " + outputFilename
        
    if (aTranscriptNameTag != None and aTranscriptCoordinateTag != None):
        command = aPythonExecutable + " " + script + " " + anInputFilename + " -o " + outputFilename + " --transcriptNameTag " + aTranscriptNameTag + " --transcriptCoordinateTag " + aTranscriptCoordinateTag + " --transcriptStrandTag " + aTranscriptStrandTag + " --minMapQual " + str(aMinMapQual) + " --log=INFO"
    else:
        command = aPythonExecutable + " " + script + " " + anInputFilename + " -o " + outputFilename + " --minMapQual " + str(aMinMapQual) + " --log=INFO"
        
    if (anRnaIncludeSecondaryAlignmentsFlag):
        command += " --rnaIncludeSecondaryAlignments"
    
    if (anIsDebug):
        logging.debug("Script: %s", script)
        logging.debug("Input: %s", anInputFilename)
        logging.debug("Output: %s", outputFilename)
        logging.debug("Filter: %s", command)
    
    readFilenameList = [script, anInputFilename]
    writeFilenameList = [outputFilename]
    if (not radiaUtil.check_for_argv_errors(None, readFilenameList, writeFilenameList)):
        sys.exit(1)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr) 
            sys.exit(1)  
            
    return outputFilename


def remove_tmpFiles(aRmTmpFilesList, aJobListFileHandler, anIsDebug):
    
    finalList = list()
    for tmpFile in aRmTmpFilesList:
        if (os.path.exists(tmpFile)):
            finalList.append("rm " + tmpFile)
            
    command = ";".join(finalList)
    
    if (anIsDebug):
        logging.debug("Command: %s", command)
    
    if (aJobListFileHandler != None):
        aJobListFileHandler.write(command + "\n")    
    else:    
        subprocessCall = subprocess.Popen(command, shell=True, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        (samtoolsStdOut, samtoolsStdErr) = subprocessCall.communicate()
        if (subprocessCall.returncode != 0):
            logging.error("The return code of '%s' from the following filter command indicates an error.", subprocessCall.returncode)
            logging.error("Error from %s:\n%s", command, samtoolsStdErr)   
            
    return


def main():
    
    #python filterRadia.py TCGA-AB-2995 12 ../data/test/TCGA-AB-2995.vcf ../data/test/ ../scripts/
    
    # create the usage statement
    usage = "usage: python %prog id chrom inputFile outputDir scriptsDir [Options]"
    i_cmdLineParser = OptionParser(usage=usage)
    
    i_cmdLineParser.add_option("-b", "--blacklistDir", dest="blacklistDir", metavar="BLACKLIST_DIR", help="the path to the blacklist directory")
    i_cmdLineParser.add_option("-t", "--targetDir", dest="targetDir", metavar="TARGET_DIR", help="the path to the exon capture targets directory")
    i_cmdLineParser.add_option("-d", "--dbSnpDir", dest="dbSnpDir", metavar="SNP_DIR", help="the path to the dbSNP directory")
    i_cmdLineParser.add_option("-r", "--retroGenesDir", dest="retroGenesDir", metavar="RETRO_DIR", help="the path to the retrogenes directory")
    i_cmdLineParser.add_option("-p", "--pseudoGenesDir", dest="pseudoGenesDir", metavar="PSEUDO_DIR", help="the path to the pseudogenes directory")
    i_cmdLineParser.add_option("-c", "--cosmicDir", dest="cosmicDir", metavar="COSMIC_DIR", help="the path to the cosmic directory")
    i_cmdLineParser.add_option("-s", "--snpEffDir", dest="snpEffDir", metavar="SNP_EFF_DIR", help="the path to the snpEff directory")
    i_cmdLineParser.add_option("-e", "--snpEffGenome", dest="snpEffGenome", default="GRCh37.75", metavar="SNP_EFF_GENOME", help="the snpEff Genome, %default by default")
    i_cmdLineParser.add_option("", "--canonical", action="store_true", default=False, dest="canonical", metavar="CANONICAL", help="include this argument if only the canonical transcripts from snpEff should be used, %default by default")
    #i_cmdLineParser.add_option("-j", "--joblistDir", dest="joblistDir", metavar="JOBLIST_DIR", help="the joblist directory")
    #i_cmdLineParser.add_option("-s", "--shebang", dest="shebang", metavar="SHEBANG", help="the shebang that should be added to the beginning of the joblist filename")
    i_cmdLineParser.add_option("-f", "--blatFastaFilename", dest="blatFastaFilename", metavar="FASTA_FILE", help="the fasta file that can be used during the BLAT filtering, default is the one specified in the VCF header")
    i_cmdLineParser.add_option("-o", "--outputFilename", dest="outputFilename", metavar="OUTPUT_FILE", help="the name of the output file, otherwise a file will be automatically created in the outputDir with the following format:  patientId + '_chr' + chrom + '.vcf')")
    
    i_cmdLineParser.add_option("", "--rnaGeneBlckFile", dest="rnaGeneBlckFile", metavar="RNA_GENE_FILE", help="the RNA gene blacklist file")
    i_cmdLineParser.add_option("", "--rnaGeneFamilyBlckFile", dest="rnaGeneFamilyBlckFile", metavar="RNA_GENE_FAMILY_FILE", help="the RNA gene family blacklist file")
    i_cmdLineParser.add_option("", "--prefix", dest="prefix", metavar="UNIQUE_FILE_PREFIX", default=None, help="a prefix to be added to all temp and output files to ensure they are unique, otherwise all files will be automatically created in the outputDir with the following format:  patientId + '_chr' + chrom + '.vcf'")
    
    # we do all filtering by default, so it's better for the user to specify --no flags to disable some filters
    # but internally, the code is nicer if we can avoid the double negatives, so store true by default and drop the "no" in the flag name
    i_cmdLineParser.add_option("", "--noBlacklist", action="store_false", default=True, dest="blacklist", help="include this argument if the blacklist filter should not be applied")
    i_cmdLineParser.add_option("", "--noTargets", action="store_false", default=True, dest="targets", help="include this argument if the target filter should not be applied")
    i_cmdLineParser.add_option("", "--noDbSnp", action="store_false", default=True, dest="dbSnp", help="include this argument if the dbSNP info/filter should not be applied")
    i_cmdLineParser.add_option("", "--noRetroGenes", action="store_false", default=True, dest="retroGenes", help="include this argument if the info/retrogenes filter should not be applied")
    i_cmdLineParser.add_option("", "--noPseudoGenes", action="store_false", default=True, dest="pseudoGenes", help="include this argument if the info/pseudogenes filter should not be applied")
    i_cmdLineParser.add_option("", "--noCosmic", action="store_false", default=True, dest="cosmic", help="include this argument if the cosmic annotation should not be applied")
    i_cmdLineParser.add_option("", "--noBlat", action="store_false", default=True, dest="blat", help="include this argument if the blat filter should not be applied")
    i_cmdLineParser.add_option("", "--noPositionalBias", action="store_false", default=True, dest="pbias", help="include this argument if the positional bias filter should not be applied")
    i_cmdLineParser.add_option("", "--noRnaBlacklist", action="store_false", default=True, dest="rnaBlacklist", help="include this argument if the RNA blacklist filter should not be applied")
    i_cmdLineParser.add_option("", "--noSnpEff", action="store_false", default=True, dest="snpEff", help="include this argument if the snpEff annotation should not be applied (without the snpEff annotation, filtering of RNA blacklisted genes will also not be applied")
    i_cmdLineParser.add_option("", "--dnaOnly", action="store_true", default=False, dest="dnaOnly", help="include this argument if you only have DNA or filtering should only be done on the DNA")
    i_cmdLineParser.add_option("", "--rnaOnly", action="store_true", default=False, dest="rnaOnly", help="include this argument if the filtering should only be done on the RNA")
    i_cmdLineParser.add_option("", "--gzip", action="store_true", default=False, dest="gzip", help="include this argument if the final VCF should be compressed with gzip")
    i_cmdLineParser.add_option("", "--transcriptNameTag", dest="transcriptNameTag", help="the INFO key where the original transcript name can be found")
    i_cmdLineParser.add_option("", "--transcriptCoordinateTag", dest="transcriptCoordinateTag", help="the INFO key where the original transcript coordinate can be found")
    i_cmdLineParser.add_option("", "--transcriptStrandTag", dest="transcriptStrandTag", help="the INFO key where the original transcript strand can be found")
    i_cmdLineParser.add_option("", "--rnaIncludeSecondaryAlignments", action="store_true", default=False, dest="rnaIncludeSecondaryAlignments", help="if you align the RNA to transcript isoforms, then you may want to include RNA secondary alignments in the samtools mpileups")
    i_cmdLineParser.add_option("", "--readSupportMinMapQual", type="int", default=int(10), dest="readSupportMinMapQual", metavar="READ_SUPPORT_MIN_MAP_QUAL", help="the minimum mapping quality for reads supporting the ALT, %default by default")
    i_cmdLineParser.add_option("", "--rnaMpileupMinMapQual", type="int", default=int(15), dest="rnaMpileupMinMapQual", metavar="RNA_MPILEUP_MIN_MAP_QUAL", help="at least 1 ALT read needs this minimum mapping quality, %default by default")
    i_cmdLineParser.add_option("", "--rnaMpileupMinAvgMapQual", type="int", default=int(20), dest="rnaMpileupMinAvgMapQual", metavar="RNA_MPILEUP_SUPPORT_MIN_MAP_QUAL", help="the minimum average mapping quality for the ALT reads, %default by default")
    
    i_cmdLineParser.add_option("-l", "--log", dest="logLevel", default="WARNING", metavar="LOG", help="the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL), %default by default")
    i_cmdLineParser.add_option("-g", "--logFilename", dest="logFilename", metavar="LOG_FILE", help="the name of the log file, STDOUT by default")
    
    # range(inclusiveFrom, exclusiveTo, by)
    i_possibleArgLengths = range(5,56,1)
    i_argLength = len(sys.argv)
    
    # check if this is one of the possible correct commands
    if (i_argLength not in i_possibleArgLengths):
        i_cmdLineParser.print_help()
        sys.exit(1)
        
    # try to use the exact python version that the user specifies on the command line
    if (sys.executable != None and sys.executable != ""):
        i_pythonExecutable = sys.executable
    else:
        i_pythonExecutable = "python"
    
    # get the required parameters
    (i_cmdLineOptions, i_cmdLineArgs) = i_cmdLineParser.parse_args()
    i_id = str(i_cmdLineArgs[0])
    i_chr = str(i_cmdLineArgs[1])
    i_inputFilename = str(i_cmdLineArgs[2])
    i_outputDir = str(i_cmdLineArgs[3])
    i_scriptsDir = str(i_cmdLineArgs[4])
    
    # get the optional params with default values   
    i_blacklistFlag = i_cmdLineOptions.blacklist
    i_rnaBlacklistFlag = i_cmdLineOptions.rnaBlacklist
    i_targetsFlag = i_cmdLineOptions.targets
    i_dbSnpFlag = i_cmdLineOptions.dbSnp
    i_retroGenesFlag = i_cmdLineOptions.retroGenes
    i_pseudoGenesFlag = i_cmdLineOptions.pseudoGenes
    i_cosmicFlag = i_cmdLineOptions.cosmic
    i_blatFlag = i_cmdLineOptions.blat
    i_pbiasFlag = i_cmdLineOptions.pbias
    i_snpEffFlag = i_cmdLineOptions.snpEff
    i_dnaOnlyFlag = i_cmdLineOptions.dnaOnly
    i_rnaOnlyFlag = i_cmdLineOptions.rnaOnly
    i_logLevel = i_cmdLineOptions.logLevel
    i_gzip = i_cmdLineOptions.gzip
    i_snpEffGenome = i_cmdLineOptions.snpEffGenome
    i_snpEffCanonical = i_cmdLineOptions.canonical
    i_rnaIncludeSecondaryAlignments = i_cmdLineOptions.rnaIncludeSecondaryAlignments
    i_readSupportMinMapQual = i_cmdLineOptions.readSupportMinMapQual
    i_rnaMpileupMinMapQual = i_cmdLineOptions.rnaMpileupMinMapQual
    i_rnaMpileupMinAvgMapQual = i_cmdLineOptions.rnaMpileupMinAvgMapQual
    
    # try to get any optional parameters with no defaults 
    i_prefix = i_id   
    i_outputFilename = None
    i_blacklistDir = None
    i_targetDir = None
    i_dbSnpDir = None
    i_retroGenesDir = None
    i_pseudoGenesDir = None
    i_cosmicDir = None
    i_joblistDir = None
    i_shebang = None
    i_logFilename = None
    i_blatFastaFilename = None
    i_snpEffDir = None
    i_rnaGeneBlckFilename = None
    i_rnaGeneFamilyBlckFilename = None
    i_transcriptNameTag = None
    i_transcriptCoordinateTag = None
    i_transcriptStrandTag = None
    readFilenameList = [i_inputFilename]  
    writeFilenameList = [i_outputDir]
    dirList = [i_scriptsDir]
    if (i_cmdLineOptions.blacklistDir != None):
        i_blacklistDir = str(i_cmdLineOptions.blacklistDir)
        dirList += [i_blacklistDir]
    if (i_cmdLineOptions.targetDir != None):
        i_targetDir = str(i_cmdLineOptions.targetDir)
        dirList += [i_targetDir]
    if (i_cmdLineOptions.dbSnpDir != None):
        i_dbSnpDir = str(i_cmdLineOptions.dbSnpDir)
        dirList += [i_dbSnpDir]
    if (i_cmdLineOptions.retroGenesDir != None):
        i_retroGenesDir = str(i_cmdLineOptions.retroGenesDir)
        dirList += [i_retroGenesDir]
    if (i_cmdLineOptions.pseudoGenesDir != None):
        i_pseudoGenesDir = str(i_cmdLineOptions.pseudoGenesDir)
        dirList += [i_pseudoGenesDir]
    if (i_cmdLineOptions.cosmicDir != None):
        i_cosmicDir = str(i_cmdLineOptions.cosmicDir)
        dirList += [i_cosmicDir]
    #if (i_cmdLineOptions.joblistDir != None):
    #    i_joblistDir = str(i_cmdLineOptions.joblistDir)
    #    dirList += [i_joblistDir]
    if (i_cmdLineOptions.snpEffDir != None):
        i_snpEffDir = str(i_cmdLineOptions.snpEffDir)
        dirList += [i_snpEffDir]
    #if (i_cmdLineOptions.shebang != None):
    #    i_shebang = str(i_cmdLineOptions.shebang)
    if (i_cmdLineOptions.outputFilename != None):
        i_outputFilename = str(i_cmdLineOptions.outputFilename)
        writeFilenameList += [i_outputFilename]
    if (i_cmdLineOptions.logFilename != None):
        i_logFilename = str(i_cmdLineOptions.logFilename)
        writeFilenameList += [i_logFilename]
    if (i_cmdLineOptions.blatFastaFilename != None):
        i_blatFastaFilename = str(i_cmdLineOptions.blatFastaFilename)
        writeFilenameList += [i_blatFastaFilename]
    if (i_cmdLineOptions.rnaGeneBlckFile != None):
        i_rnaGeneBlckFilename = str(i_cmdLineOptions.rnaGeneBlckFile)
        readFilenameList += [i_rnaGeneBlckFilename]
    if (i_cmdLineOptions.rnaGeneFamilyBlckFile != None):
        i_rnaGeneFamilyBlckFilename = str(i_cmdLineOptions.rnaGeneFamilyBlckFile)
        readFilenameList += [i_rnaGeneFamilyBlckFilename]
    if (i_cmdLineOptions.transcriptNameTag != None):
        i_transcriptNameTag = i_cmdLineOptions.transcriptNameTag
    if (i_cmdLineOptions.transcriptCoordinateTag != None):
        i_transcriptCoordinateTag = i_cmdLineOptions.transcriptCoordinateTag
    if (i_cmdLineOptions.transcriptStrandTag != None):
        i_transcriptStrandTag = i_cmdLineOptions.transcriptStrandTag
    if (i_cmdLineOptions.prefix != None):
        i_prefix = i_cmdLineOptions.prefix    
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    i_numericLogLevel = getattr(logging, i_logLevel.upper(), None)
    if not isinstance(i_numericLogLevel, int):
        raise ValueError("Invalid log level: '%s' must be one of the following:  DEBUG, INFO, WARNING, ERROR, CRITICAL", i_logLevel)
    
    # set up the logging
    if (i_logFilename != None):
        logging.basicConfig(level=i_numericLogLevel, filename=i_logFilename, filemode='w', format='%(asctime)s\t%(levelname)s\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    else:
        logging.basicConfig(level=i_numericLogLevel, format='%(asctime)s\t%(levelname)s\t%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        
    # set the debug    
    i_debug = (i_numericLogLevel == logging.DEBUG)

    # do some debugging
    if (i_debug):
        logging.debug("pythonExecutable=%s", i_pythonExecutable)
        logging.debug("id=%s", i_id)
        logging.debug("chr=%s", i_chr)
        logging.debug("inputFilename=%s", i_inputFilename)
        logging.debug("outputFilename=%s", i_outputFilename)
        logging.debug("outputDir=%s", i_outputDir)
        logging.debug("scriptsDir=%s", i_scriptsDir)
        logging.debug("logLevel=%s", i_logLevel)
        logging.debug("gzip=%s", i_gzip)
        logging.debug("logFile=%s", i_logFilename)
        logging.debug("prefix=%s", i_prefix)
        logging.debug("blatfastaFile=%s", i_blatFastaFilename)
        logging.debug("rnaGeneBlckFilename=%s", i_rnaGeneBlckFilename)
        logging.debug("rnaGeneFamilyBlckFilename=%s", i_rnaGeneFamilyBlckFilename)
        logging.debug("blacklistFlag? %s", i_blacklistFlag)
        logging.debug("rnaBlacklistFlag? %s", i_rnaBlacklistFlag)
        logging.debug("targetsFlag? %s", i_targetsFlag)
        logging.debug("dbSnpFlag? %s", i_dbSnpFlag)
        logging.debug("snpEffFlag? %s", i_snpEffFlag)
        logging.debug("retroGenesFlag? %s", i_retroGenesFlag)
        logging.debug("pseudoGenesFlag? %s", i_pseudoGenesFlag)
        logging.debug("cosmicFlag? %s", i_cosmicFlag)
        logging.debug("blatFlag? %s", i_blatFlag)
        logging.debug("pbiasFlag? %s", i_pbiasFlag)
        logging.debug("dnaOnlyFlag? %s", i_dnaOnlyFlag)
        logging.debug("rnaOnlyFlag? %s", i_rnaOnlyFlag)
        logging.debug("blacklistDir %s", i_blacklistDir)
        logging.debug("targetDir %s", i_targetDir)
        logging.debug("dbSnpDir %s", i_dbSnpDir)
        logging.debug("snpEffDir %s", i_snpEffDir)
        logging.debug("snpEffGenome %s", i_snpEffGenome)
        logging.debug("snpEffCanonical %s", i_snpEffCanonical)
        logging.debug("retroGenesDir %s", i_retroGenesDir)
        logging.debug("pseudoGenesDir %s", i_pseudoGenesDir)
        logging.debug("cosmicDir %s", i_cosmicDir)
        logging.debug("joblistDir %s", i_joblistDir)
        logging.debug("transcriptNameTag %s", i_transcriptNameTag)
        logging.debug("transcriptCoordinateTag %s", i_transcriptCoordinateTag)
        logging.debug("transcriptStrandTag %s", i_transcriptStrandTag)
        logging.debug("rnaIncludeSecondaryAlignments=%s" % i_rnaIncludeSecondaryAlignments)
        logging.debug("readSupportMinMapQual=%s" % i_readSupportMinMapQual)
        logging.debug("rnaMpileupMinMapQual=%s" % i_rnaMpileupMinMapQual)
        logging.debug("rnaMpileupMinAvgMapQual=%s" % i_rnaMpileupMinAvgMapQual)
     
    if (i_dnaOnlyFlag):
        i_rnaBlacklistFlag = False
        
    if (i_blacklistFlag):
        if (i_blacklistDir == None):
            logging.critical("No blacklist directory has been specified.")
            sys.exit(1)
    
    if (i_dbSnpFlag):
        if (i_dbSnpDir == None):
            logging.critical("No dbSNP directory has been specified.")
            sys.exit(1)
    
    if (i_retroGenesFlag):
        if (i_retroGenesDir == None):
            logging.critical("No retrogenes directory has been specified.")
            sys.exit(1)

    if (i_pseudoGenesFlag):
        if (i_pseudoGenesDir == None):
            logging.critical("No pseudogenes directory has been specified.")
            sys.exit(1)
    
    if (i_cosmicFlag):
        if (i_cosmicDir == None):
            logging.critical("No COSMIC directory has been specified.")
            sys.exit(1)
    
    if (i_targetsFlag):
        if (i_targetDir == None):
            logging.critical("No exome capture target directory has been specified.")
            sys.exit(1)
            
    if (i_snpEffFlag):
        if (i_snpEffDir == None):
            logging.critical("No snpEff directory has been specified.")
            sys.exit(1)
    
    if (i_rnaBlacklistFlag):
        if (i_rnaGeneBlckFilename == None):
            logging.critical("No RNA gene blacklist has been specified.")
            sys.exit(1)
        if (i_rnaGeneFamilyBlckFilename == None):
            logging.critical("No RNA gene family blacklist has been specified.")
            sys.exit(1)
    
    # check to see if the files exist
    if (not radiaUtil.check_for_argv_errors(dirList, readFilenameList, writeFilenameList)):
        sys.exit(1)           
    
    i_joblistFileHandler = None
    if (i_joblistDir != None):
        i_joblistFileHandler = get_write_fileHandler(os.path.join(i_joblistDir, i_id + "_chr" + i_chr + ".sh"))
        if (i_shebang != None):
            i_joblistFileHandler.write(i_shebang + "\n")
    
    previousFilename = i_inputFilename
    rmTmpFilesList = list()
    
    if (i_dnaOnlyFlag):
        # filter by blacklist
        if (i_blacklistFlag):
            previousFilename = filter_blacklist(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_blacklistDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
           
        # flag snp
        if (i_dbSnpFlag):
            previousFilename = flag_dbSnp(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_dbSnpDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
        
        # flag retro genes
        if (i_retroGenesFlag):                
            previousFilename = flag_retroGenes(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_retroGenesDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
    
        # flag pseudo genes
        if (i_pseudoGenesFlag):
            previousFilename = flag_pseudoGenes(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_pseudoGenesDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
    
        # flag cosmic
        if (i_cosmicFlag):                
            previousFilename = flag_cosmic(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_cosmicDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
        
        # filter targets
        if (i_targetsFlag):            
            previousFilename = filter_targets(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_targetDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
        
        # filter mpileup
        previousFilename = filter_mpileupSupport_dna(i_pythonExecutable, i_id, i_chr, previousFilename, None, True, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(previousFilename)
        
    else:        
        # filter by blacklist
        if (i_blacklistFlag):    
            previousFilename = filter_blacklist(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_blacklistDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
            
        # filter by dbsnp
        if (i_dbSnpFlag):
            previousFilename = flag_dbSnp(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_dbSnpDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)

        # flag retro genes
        if (i_retroGenesFlag):
            previousFilename = flag_retroGenes(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_retroGenesDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
    
        # flag pseudo genes
        if (i_pseudoGenesFlag):
            previousFilename = flag_pseudoGenes(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_pseudoGenesDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
        
        # flag cosmic
        if (i_cosmicFlag):
            previousFilename = flag_cosmic(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_cosmicDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
        
        # filter targets
        if (i_targetsFlag):
            previousFilename = filter_targets(i_pythonExecutable, i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_targetDir, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
    
        # filter RNA mpileup
        # the output file contains all filters for all possible mod types and no final mod type is chosen
        rnaFilename = filter_mpileupSupport_rna(i_pythonExecutable, i_id, i_chr, previousFilename, True, i_rnaMpileupMinMapQual, i_rnaMpileupMinAvgMapQual, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(rnaFilename)
        
        # filter DNA mpileup
        # the output file contains all filters for all possible mod types and no final mod type is chosen
        dnaFilename = filter_mpileupSupport_dna(i_pythonExecutable, i_id, i_chr, previousFilename, None, True, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(dnaFilename)
        
        # compare the rna and dna
        # calls that pass in both the DNA and RNA will be in the overlaps file
        # calls that don't pass in the DNA but pass in the RNA are in the non-overlaps file - these are the RNA Rescue and RNA Editing calls
        (overlapFilename, nonoverlapFilename) = radia_compare(i_pythonExecutable, i_id, i_chr, rnaFilename, dnaFilename, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(overlapFilename)
        rmTmpFilesList.append(nonoverlapFilename)
        
        # filter DNA mpileup
        # filter the RNA Rescue and RNA Editing calls based on the DNA to get rid of any possible germline calls
        previousFilename = filter_mpileupSupport_dna(i_pythonExecutable, i_id, i_chr, nonoverlapFilename, dnaFilename, False, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(previousFilename)
        
        # filter out possible germline calls
        previousFilename = filter_rnaOnly(i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(previousFilename)
        
        # if we have something to blat
        if (os.path.isfile(previousFilename) and os.stat(previousFilename).st_size > 20):
            
            # the blat input is needed for the blat and pbias filters
            if (i_blatFlag or i_pbiasFlag):
                # create blat input
                blatInputFilename = filter_createBlatInput(i_pythonExecutable, i_id, i_chr, previousFilename, rnaFilename, i_transcriptNameTag, i_transcriptCoordinateTag, i_transcriptStrandTag, i_rnaIncludeSecondaryAlignments, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_debug)
                rmTmpFilesList.append(blatInputFilename)
            
            # filter by BLAT
            if (i_blatFlag):    
                (blatOutputFilename, previousFilename) = filter_blat(i_pythonExecutable, i_id, i_chr, previousFilename, rnaFilename, blatInputFilename, i_blatFastaFilename, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
                rmTmpFilesList.append(blatOutputFilename)
                rmTmpFilesList.append(previousFilename)
            
            # the blat input is needed
            if (i_pbiasFlag and os.path.isfile(previousFilename) and os.stat(previousFilename).st_size > 20):
                # if we filtered via blat, then keep the previous filters so that the blat filter gets passed on
                if (i_blatFlag):
                    # filter by positional bias
                    previousFilename = filter_positionalBias(i_pythonExecutable, i_id, i_chr, previousFilename, blatInputFilename, True, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
                # if we didn't filter via blat, then don't keep the previous filters
                else:
                    # filter by positional bias
                    previousFilename = filter_positionalBias(i_pythonExecutable, i_id, i_chr, previousFilename, blatInputFilename, False, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
                rmTmpFilesList.append(previousFilename)
                
        # if RNA only, just merge the RNA Confirmation and RNA Rescue calls
        if (i_rnaOnlyFlag):
            # the dnaFilename and --dnaHeaderOnly=True means that we only extract the header from the dnaFilename and ignore the rest
            previousFilename = merge_rnaAndDna(i_pythonExecutable, i_id, i_chr, dnaFilename, rnaFilename, overlapFilename, previousFilename, True, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
        else:
            # merge RNA and DNA
            # the dnaFilename and --dnaHeaderOnly=False means that we merge the header and the results in the dnaFilename
            previousFilename = merge_rnaAndDna(i_pythonExecutable, i_id, i_chr, dnaFilename, rnaFilename, overlapFilename, previousFilename, False, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
        
    if (i_snpEffFlag):
        # keep track of the orginal file
        preSnpEffFilename = previousFilename
        
        # extracting passing calls
        previousFilename = extract_passing(i_id, i_chr, previousFilename, i_outputDir, i_prefix, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(previousFilename)
      
        previousFilename = filter_runSnpEff(i_id, i_chr, previousFilename, i_snpEffDir, i_snpEffGenome, i_snpEffCanonical, i_outputDir, i_prefix, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(previousFilename)
    
        if (not i_dnaOnlyFlag and i_rnaBlacklistFlag):
            # filter RNA by geneNames/Families
            previousFilename = filter_rnaBlacklist(i_pythonExecutable, i_id, i_chr, previousFilename, i_rnaGeneBlckFilename, i_rnaGeneFamilyBlckFilename, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
            rmTmpFilesList.append(previousFilename)
    
        # merge passing with snpEff back with originals 
        previousFilename = merge_passingAndOriginals(i_pythonExecutable, i_id, i_chr, previousFilename, preSnpEffFilename, i_outputDir, i_prefix, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
        rmTmpFilesList.append(previousFilename)
                    
    # everything gets run through the read support filter
    previousFilename = filter_readSupport(i_pythonExecutable, i_id, i_chr, previousFilename, i_transcriptNameTag, i_transcriptCoordinateTag, i_transcriptStrandTag, i_rnaIncludeSecondaryAlignments, i_readSupportMinMapQual, i_outputDir, i_prefix, i_outputFilename, i_scriptsDir, i_joblistFileHandler, i_gzip, i_debug)
    
    # if we aren't debugging, then remove all the tmp files
    if (not i_debug):
        # remove all the temp files
        remove_tmpFiles(rmTmpFilesList, i_joblistFileHandler, i_debug)
        
    if (i_joblistDir != None):
        i_joblistFileHandler.close()
        
    return

main()
sys.exit(0)
