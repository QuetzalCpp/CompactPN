# python test.py --model posenet --dataroot ./datasets/gps --name posenet/gps/beta100 --gpu 0 --phase scene1_validation2_test
# --phase is the file name with validation or test images
import time
import os
from options.test_options import TestOptions
from data.data_loader import CreateDataLoader
from models.models import create_model
from util.visualizer import Visualizer
from util import html
import numpy

opt = TestOptions().parse()
opt.nThreads = 1   # test code only supports nThreads = 1
opt.batchSize = 1  # test code only supports batchSize = 1
opt.serial_batches = True  # no shuffle
opt.no_flip = True  # no flip

data_loader = CreateDataLoader(opt)
dataset = data_loader.load_data()

results_dir = os.path.join(opt.results_dir, opt.name)
if not os.path.exists(results_dir):
    os.makedirs(results_dir)

besterror  = [0, float('inf'), float('inf')] # nepoch, medX, medQ
if opt.model == 'posenet':
    testepochs = numpy.arange(450, 1000+1, 5)
    #testepochs = numpy.arange(450, 500+1, 5)
else:
    testepochs = numpy.arange(450, 1000+1, 5)
    #testepochs = numpy.arange(450, 500+1, 5)

testfile = open(os.path.join(results_dir, 'test_median.txt'), 'a')
testfile.write('epoch medX  medQ\n')
testfile.write('==================\n')

testfile2 = open(os.path.join(results_dir, 'test_mean.txt'), 'a')
testfile2.write('epoch medX  medQ\n')
testfile2.write('==================\n')

testfile3 = open(os.path.join(results_dir, 'test_std.txt'), 'a')
testfile3.write('epoch medX  medQ\n')
testfile3.write('==================\n')

model = create_model(opt)
visualizer = Visualizer(opt)

for testepoch in testepochs:
    model.load_network(model.netG, 'G', testepoch)
    visualizer.change_log_path(testepoch)
    # test
    # err_pos = []
    # err_ori = []
    err = []
    print("========================= epoch: "+ str(testepoch) + "==========================")
    results = numpy.zeros((len(dataset),1))
    for i, data in enumerate(dataset):
        model.set_input(data)
        model.test()
        img_path = model.get_image_paths()[0]
        #print('\t%04d/%04d: process image... %s' % (i, len(dataset), img_path), end='\r')
        #print('\t%04d/%04d: process image... %s' % (i, len(dataset), img_path))
        image_path = img_path.split('/')[-2] + '/' + img_path.split('/')[-1]
        pose = model.get_current_pose()
        visualizer.save_estimated_pose(image_path, pose)
        err_p = model.get_current_errors()
        #err_p, err_o = model.get_current_errors()
        # err_pos.append(err_p)
        # err_ori.append(err_o)
        #err.append([err_p, err_o])
        
        #print("Error_pose", err_p)
        results[i, :] = numpy.asarray([err_p])
        #err.append([err_p])

    median_pos = numpy.median(results, axis=0)
    mean_pos = numpy.mean(results, axis=0)
    #median_pos = numpy.median(err, axis=0)
    staan = numpy.std(results, axis=0)
    print("std", staan[0])
    print('Median error ', median_pos[0])
    print('Mean error ', mean_pos[0])

    if median_pos[0] < besterror[1]:
        besterror = [testepoch, median_pos[0]]
        #besterror = [testepoch, median_pos[0], median_pos[1]]
    #print()
    #print("median position: {0:.2f}".format(numpy.median(results)))
    # print("median orientat: {0:.2f}".format(numpy.median(err_ori)))
    print("\tmedian wrt pos.: {0:.2f}m".format(float(median_pos[0])))
    #print("\tmedian wrt pos.: {0:.2f}m {1:.2f} degree".format(median_pos[0], median_pos[1]))
    #testfile.write("{0:<5} {1:.2f}m {2:.2f}degree\n".format(testepoch,median_pos[0],median_pos[1]))
    testfile.write("{0:<5} {1:.2f}m\n".format(testepoch, float(median_pos[0])))
    testfile.flush()

    testfile2.write("{0:<5} {1:.2f}m\n".format(testepoch, float(mean_pos[0])))
    testfile2.flush()

    testfile3.write("{0:<5} {1:.2f}m\n".format(testepoch, float(staan[0])))
    testfile3.flush()
#print("{0:<5} {1:.2f}m {2:.2f}degree\n".format(*besterror))
#print("{0:<5} {1:.2f}m".format(besterror[0], float(besterror[1])))
testfile.write('-----------------\n')
#testfile.write("{0:<5} {1:.2f}m {2:.2f}degree\n".format(*besterror))
testfile.write("{0:<5} {1:.2f}m\n".format(besterror[0], float(besterror[1])))
testfile.write('==================\n')
testfile.close()
testfile2.close()
testfile3.close()