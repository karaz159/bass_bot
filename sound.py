from pysndfx import AudioEffectsChain as af

apply_af = af().lowshelf(50)

infile = 'sound.wav'
outfile = 'out.wav'

apply_af(infile, outfile)
print ('done')
