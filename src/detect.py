import sys

import double_jpeg_compression
import copy_move_cfa
import copy_move_detection
import noise_variance

from optparse import OptionParser

if __name__ == '__main__':
    # copy-move parameters
    cmd = OptionParser("usage: %prog image_file [options]")
    cmd.add_option('', '--imauto', help='Automatically search identical regions. (default: %default)', default=1)
    cmd.add_option('', '--imblev',help='Blur level for degrading image details. (default: %default)', default=8)
    cmd.add_option('', '--impalred',help='Image palette reduction factor. (default: %default)', default=15)
    cmd.add_option('', '--rgsim', help='Region similarity threshold. (default: %default)', default=5)
    cmd.add_option('', '--rgsize',help='Region size threshold. (default: %default)', default=1.5)
    cmd.add_option('', '--blsim', help='Block similarity threshold. (default: %default)',default=200)
    cmd.add_option('', '--blcoldev', help='Block color deviation threshold. (default: %default)', default=0.2)
    cmd.add_option('', '--blint', help='Block intersection threshold. (default: %default)', default=0.2)
    opt, args = cmd.parse_args()
    if not args:
        cmd.print_help()
        sys.exit()
    im_str = args[0]

    print('\nIs double compressed: ')
    double_compressed = double_jpeg_compression.detect('..//images//' + im_str)

    if(double_compressed): print('\tTRUE')
    else: print('\tFALSE')

    print('\nNoise variance inconsistency detected: ')
    noise_forgery = noise_variance.detect('..//images//' + im_str)

    if(noise_forgery): print('\tTRUE')
    else: print('\tFALSE')

    print('\nCopy-move regions found: ')
    #print('\nRunning CFA artifact detection...\n')
    identical_regions_cfa = copy_move_cfa.detect('..//images//' + im_str, opt, args)
    #print('\n', identical_regions_cfa, 'CFA artifacts detected')

    count_cmf = copy_move_detection.detect('../images/', im_str, '../output/', blockSize=32)
    if(identical_regions_cfa != 0):
        if(count_cmf != 0):
            print(count_cmf, 'identical regions detected')
            identical_regions_cfa = 0
            if(count_cmf == 0):
                print(identical_regions_cfa, 'identical regions detected')
    else:
        print(count_cmf, 'identical regions detected')

    if ((not double_compressed) and (identical_regions_cfa == 0) and (not noise_forgery) and (count_cmf == 0)):
        print('\nNo forgeries were detected - this image has probably not been tampered with.')
    else:
        print('\nSome forgeries were detected - this image may have been tampered with.')
