class ASNeck(nn.Module):
    def __init__(self, h, w, in_channels, out_channels, p=0.01):
        
        super().__init__()
        
        # Define class variables
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.h = h
        self.w = w
        
        self.dropout = nn.Dropout2d(p=p)
        
        self.conv1 = nn.Conv2d(in_channels = self.in_channels,
                               out_channels = self.out_channels,
                               kernel_size = 1,
                               stride = 1,
                               padding = 0,
                               bias = False)
        
        self.prelu1 = nn.PReLU()
        
        self.conv21 = nn.Conv2d(in_channels = self.out_channels,
                                  out_channels = self.out_channels,
                                  kernel_size = (1, 5),
                                  stride = 1,
                                  padding = (0, 2),
                                  bias = True)
        
        self.conv22 = nn.Conv2d(in_channels = self.out_channels,
                                  out_channels = self.out_channels,
                                  kernel_size = (5, 1),
                                  stride = 1,
                                  padding = (2, 0),
                                  bias = True)
        
        self.prelu2 = nn.PReLU()
        
        self.conv3 = nn.Conv2d(in_channels = self.out_channels,
                                  out_channels = self.out_channels,
                                  kernel_size = 1,
                                  stride = 1,
                                  padding = 0,
                                  bias = False)
        
        self.prelu3 = nn.PReLU()
        
        self.batchnorm = nn.BatchNorm2d(self.out_channels)
        
    def forward(self, x):
        bs = x.size()[0]
        x_copy = x.clone()
        
        # Side Branch
        x = self.conv1(x)
        x = self.batchnorm(x)
        x = self.prelu1(x)
        
        x = self.conv21(x)
        x = self.conv22(x)
        x = self.batchnorm(x)
        x = self.prelu2(x)
        
        x = self.conv3(x)
        x = self.batchnorm(x)
                
        x = self.dropout(x)
        
        # Main Branch
        
        if self.in_channels != self.out_channels:
            out_shape = self.out_channels - self.in_channels
            extras = torch.zeros((bs, out_shape, x.shape[2], x.shape[3]))
            print (x_copy.shape, extras.shape)
            x_copy = torch.cat((x_copy, extras), dim = 1)
        
        print (x.shape, x_copy.shape)
        # Sum of main and side branches
        x = x + x_copy
        x = self.prelu3(x)
        
        return x