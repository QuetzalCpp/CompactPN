import numpy as np
import torch
import torch.nn.functional as F
import os
from collections import OrderedDict
from torch.autograd import Variable
import util.util as util
from util.image_pool import ImagePool
from .base_model import BaseModel
from . import networks
import pickle
import numpy

class PoseLSTModel(BaseModel):
    def name(self):
        return 'PoseLSTModel'

    def initialize(self, opt):
        BaseModel.initialize(self, opt)
        self.isTrain = opt.isTrain
        # define tensors
        self.input_A = self.Tensor(opt.batchSize, opt.input_nc,opt.fineSize, opt.fineSize) #75,3,224,224
        self.input_B = self.Tensor(opt.batchSize, opt.output_nc) # 75, 7--> x,y,z,p,q,r,w

        # load/define networks
        googlenet_weights = None
        if self.isTrain and opt.init_weights != '':
            googlenet_file = open(opt.init_weights, "rb")
            googlenet_weights = pickle.load(googlenet_file)
            googlenet_file.close()
            print('initializing the weights from '+ opt.init_weights)
        self.mean_image = np.load(os.path.join(opt.dataroot , 'mean_image.npy'))

        self.netG = networks.define_network(opt.input_nc, opt.lstm_hidden_size, opt.model,
                                      init_from=googlenet_weights, isTest=not self.isTrain,
                                      gpu_ids = self.gpu_ids)

        if not self.isTrain or opt.continue_train:
            self.load_network(self.netG, 'G', opt.which_epoch)

        if self.isTrain:
            self.old_lr = opt.lr
            # define loss functions
            self.criterion = torch.nn.MSELoss()

            # initialize optimizers
            self.schedulers = []
            self.optimizers = []
            self.optimizer_G = torch.optim.Adam(self.netG.parameters(),
                                                lr=opt.lr, eps=1,
                                                weight_decay=0.0625,
                                                betas=(self.opt.adambeta1, self.opt.adambeta2))
            self.optimizers.append(self.optimizer_G)
            # for optimizer in self.optimizers:
            #     self.schedulers.append(networks.get_scheduler(optimizer, opt))

        print('---------- Networks initialized -------------')
        # networks.print_network(self.netG)
        # print('-----------------------------------------------')

    def set_input(self, input):
        input_A = input['A']
        input_B = input['B']
        self.image_paths = input['A_paths']
        self.input_A.resize_(input_A.size()).copy_(input_A)
        self.input_B.resize_(input_B.size()).copy_(input_B)

    def forward(self):
        self.pred_B = self.netG(self.input_A)

    # no backprop gradients
    def test(self):
        self.forward()

    # get image paths
    def get_image_paths(self):
        return self.image_paths

    def backward(self):
        self.loss_G = 0
        self.loss_pos = 0 # x,y,z
        #self.loss_ori = 0 # p,q,r,w
        loss_weights = [0.3, 0.3, 1]
        for l, w in enumerate(loss_weights):
            mse_pos = self.criterion(self.pred_B[2*l], self.input_B[:, 0:3])
            #ori_gt = F.normalize(self.input_B[:, 3:], p=2, dim=1)
            #mse_ori = self.criterion(self.pred_B[2*l+1], ori_gt)
            #self.loss_G += (mse_pos + mse_ori * self.opt.beta) * w
            self.loss_G += (mse_pos * self.opt.beta) * w
            self.loss_pos += mse_pos.item() * w
            #self.loss_ori += mse_ori.item() * w * self.opt.beta
        self.loss_G.backward()

    def optimize_parameters(self):
        self.forward()
        self.optimizer_G.zero_grad()
        self.backward()
        self.optimizer_G.step()

    def get_current_errors(self):
        if self.opt.isTrain:
            return OrderedDict([('pos_err', self.loss_pos)])#,
                                #('ori_err', self.loss_ori),
                                #])

        pos_err = torch.dist(self.pred_B[0], self.input_B[:, 0:3])
        #ori_gt = F.normalize(self.input_B[:, 3:], p=2, dim=1)
        #abs_distance = torch.abs((ori_gt.mul(self.pred_B[1])).sum())
        #ori_err = 2*180/numpy.pi* torch.acos(abs_distance)
        #return [pos_err.item(), ori_err.item()]
        return [pos_err.item()]

    def get_current_pose(self):
        return numpy.concatenate((self.pred_B[0].data[0].cpu().numpy(),
                                  self.pred_B[1].data[0].cpu().numpy()))

    def get_current_visuals(self):
        input_A = util.tensor2im(self.input_A.data)
        # pred_B = util.tensor2im(self.pred_B.data)
        # input_B = util.tensor2im(self.input_B.data)
        return OrderedDict([('input_A', input_A)])

    def save(self, label):
        self.save_network(self.netG, 'G', label, self.gpu_ids)
