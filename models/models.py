
def create_model(opt):
    model = None
    print(opt.model)
    if opt.model == 'posenet':
        from .posenet_model import PoseNetModel
        model = PoseNetModel()
    elif opt.model == 'poselstm':
        from .poselstm_model import PoseLSTModel
        model = PoseLSTModel()
    elif opt.model == 'compactPN1':
        from .compactPN1 import compactPN1Model
        model = compactPN1Model()
    elif opt.model == 'compactPN2':
        from .compactPN2 import compactPN2Model
        model = compactPN2Model()
    elif opt.model == 'compactPN3':
        from .compactPN3 import compactPN3Model
        model = compactPN3Model()
    else:
        raise ValueError("Model [%s] not recognized." % opt.model)
    model.initialize(opt)
    print("model [%s] was created" % (model.name()))
    return model
