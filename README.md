# CompactPN: Convolutional Neural Networks for Geo-Localisation with a Single Aerial Image

Nowadays, Unmanned Aerial Vehicles (UAVs) navigating outdoors rely heavily on GPS for localisation and autonomous flight or  applications for aerial photography recording with a GPS coordinate. However, GPS may fail or become unreliable, thus compromising the flight mission. Motivated by this scenario, in this work, we present a study on the use of popular Convolutional Neural Networks (CNN) to address the problem of geo-localisation from a single aerial image. We compare CNN-based architectures from the state of the art, and introduce a compact architecture to speed up the inference process without affecting the estimation error. For our experiments, aerial images were recorded with a monocular camera on board a UAV, flying outdoors with a height between 20 to 25 metres. On average, our compact network achieves a minimum estimation error of 2.8 metres and a maximum of 6.1 metres, which is comparable to the performance of other networks in the state of the art. However, our network achieves on average an operation frequency of 103 fps versus 69 fps achieved by the fastest network in the comparison analysis. These results are promising since such speed would enable fast geo-localisation with cameras capturing images at those frame rates, which are useful for obtaining neater images than with conventional cameras working at 30 fps.

<p align="center">
  <img src="images/figure1.png">
</p>

## Overview of our approach

![alt text](images/overview_approach.jpg)

It consists of 4 steps: (1) Data acquisition using the drone’s onboard camera; (2) Real-time mosaic generation, consisting of 6 frames; (3) Flight commands prediction using our proposed CNN named DeepPilot, these commands are represented by the tuple (ϕ,θ,ψ,h); (4) Implementation of a filter to smooth the signal.

## DeepPilot Architecture
Our proposed DeepPilot runs 3 specialized models in parallel. The first one predicts ϕ and θ angular positions of the body frame; the second one predicts ψ, the rotational speed over the Z-axis; and the third one predicts h, the vertical speed. The size of the kernels is indicated in the colored boxes at the bottom-left.

![alt text](images/DeepPilot_architecture.jpg)

## Video
A video of this approach can be watched at: https://youtu.be/Qo48pRCxM40.

[![Watch the video](images/gate5.gif)](https://www.youtube.com/watch?v=YD5oqe8DelE)

[![Watch the video](https://i9.ytimg.com/vi/Qo48pRCxM40/mq2.jpg?sqp=COjn1fkF&rs=AOn4CLAn53ux1V39jaAOEYNxewph9vDDYA)](https://www.youtube.com/watch?v=YD5oqe8DelE)
[![Watch the video](https://i9.ytimg.com/vi/Qo48pRCxM40/mq3.jpg?sqp=COjn1fkF&rs=AOn4CLAT5O0iM-yuXqo-VJ0grnLhrh56EQ)](https://www.youtube.com/watch?v=YD5oqe8DelE)

## Recommended system
- Ubuntu 16.04
- ROS kinetic Kame
- Python 2.7.15
- Cuda 9.0
- Cudnn 7.3.0
- Tensorflow 1.12.0
- Keras 2.2.4
- Tum_simulator ported to Kinetic (https://github.com/angelsantamaria/tum_simulator.git)

## DeepPilot

```bash
git clone https://github.com/QuetzalCpp/DeepPilot.git
cd DeepPilot
```

### Additional Resources
- [DeepPilot Models pretrained](https://inaoepedu-my.sharepoint.com/:f:/g/personal/carranza_inaoe_edu_mx/EslxVDqc9zBMmiV4mDH48KUBAcAHu0Ypt1rZLL6ifOjyoA?e=VYtMyT)
- [Datasets to train DeepPilot](https://inaoepedu-my.sharepoint.com/:f:/g/personal/carranza_inaoe_edu_mx/EslxVDqc9zBMmiV4mDH48KUBAcAHu0Ypt1rZLL6ifOjyoA?e=VYtMyT)

### Train DeepPilot

```bash
cd /bebop_ws/src/DeepPilot/DeepPilot_network
python train_deeppilot.py
```

### Start DeepPilot

```bash
cd /bebop_ws/src/DeepPilot/DeepPilot_network
python evaluation_mosaic-6img.py
```

## Reference
If you use any of data, model or code, please cite the following reference:

Rojas-Perez, L.O., & Martinez-Carranza, J. (2020). DeepPilot: A CNN for Autonomous Drone Racing. Sensors, 20(16), 4524.
https://doi.org/10.3390/s20164524

```
@article{rojas2020deeppilot,
  title={DeepPilot: A CNN for Autonomous Drone Racing},
  author={Rojas-Perez, Leticia Oyuki and Martinez-Carranza, Jose},
  journal={Sensors},
  volume={20},
  number={16},
  pages={4524},
  year={2020},
  publisher={Multidisciplinary Digital Publishing Institute}
}
```
## Related References

- L. O. Rojas-Perez and J. Martinez-Carranza, "Autonomous Drone Racing with an Opponent:  A First Approach",Computación y Sistemas (2020).
```
@article{rojas2020ADRwithop,
  title={Autonomous Drone Racing with an Opponent:  A First Approach},
  author={Rojas-Perez, Leticia Oyuki and Martinez-Carranza, Jose},
  journal={Computaci{\'o}n y Sistemas},
  volume={},
  number={},
  year={2020}
}
```

- A. A. Cabrera-Ponce, L. O. Rojas-Perez, J. A. Carrasco-Ochoa, J. F. Martinez-Trinidad and J. Martinez-Carranza, "Gate Detection for Micro Aerial Vehicles using a Single Shot Detector," in IEEE Latin America Transactions, vol. 17, no. 12, pp. 2045-2052, December 2019, doi: 10.1109/TLA.2019.9011550.

```
@ARTICLE{9011550,
  author={A. A. {Cabrera-Ponce} and L. O. {Rojas-Perez} and J. A. {Carrasco-Ochoa} and J. F. {Martinez-Trinidad} and J. {Martinez-Carranza}},
  journal={IEEE Latin America Transactions}, 
  title={Gate Detection for Micro Aerial Vehicles using a Single Shot Detector}, 
  year={2019},
  volume={17},
  number={12},
  pages={2045-2052},}
```

- L. O. Rojas-Perez and J. Martinez-Carranza, "A Temporal CNN-based Approach for Autonomous Drone Racing," 2019 Workshop on Research, Education and Development of Unmanned Aerial Systems (RED UAS), Cranfield, United Kingdom, 2019, pp. 70-77, doi: 10.1109/REDUAS47371.2019.8999703.
```
@INPROCEEDINGS{8999703,
  author={L. O. {Rojas-Perez} and J. {Martinez-Carranza}},
  booktitle={2019 Workshop on Research, Education and Development of Unmanned Aerial Systems (RED UAS)}, 
  title={A Temporal CNN-based Approach for Autonomous Drone Racing}, 
  year={2019},
  volume={},
  number={},
  pages={70-77},}
```

- J. A. Cocoma-Ortega, L. O. Rojas-Perez, A. A. Cabrera-Ponce and J. Martinez-Carranza, "Overcoming the Blind Spot in CNN-based Gate Detection for Autonomous Drone Racing," 2019 Workshop on Research, Education and Development of Unmanned Aerial Systems (RED UAS), Cranfield, United Kingdom, 2019, pp. 253-259, doi: 10.1109/REDUAS47371.2019.8999722.

```
@INPROCEEDINGS{8999722,
  author={J. A. {Cocoma-Ortega} and L. O. {Rojas-Perez} and A. A. {Cabrera-Ponce} and J. {Martinez-Carranza}},
  booktitle={2019 Workshop on Research, Education and Development of Unmanned Aerial Systems (RED UAS)}, 
  title={Overcoming the Blind Spot in CNN-based Gate Detection for Autonomous Drone Racing}, 
  year={2019},
  volume={},
  number={},
  pages={253-259},}
```

 ## Acknowledgements
We are thankful for the processing time granted by the National Laboratory of Supercomputing (LNS) under the project 201902063C. The first author is thankful to Consejo Nacional de Ciencia y Tecnología (CONACYT) for the scholarship No. 924254. We are also thankful for the partial financial support granted via the FORDECYT project no. 296737 “Consorcio en Inteligencia Artificial” for the development of this work.
