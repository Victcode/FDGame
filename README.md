# FDGame

FDGame(Freedom Dance Game) is a dance game that can be run on a laptop. It has the following characteristics:

- You can use any music you like.
- There is no fixed action limit, to provide free play space for players.

At present, it's only the primary version, and the next optimization job:

- [ ] Improve accuracy of HPE;
- [ ] Optimizing action instruction;



## Table of Contents

- [FDGame](#fdgame)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Music Process<a name="music-process"/>](#music-processa-namemusic-process)
  - [Game Play<a name="game-play"/>](#game-playa-namegame-play)
  - [Citation:](#citation)

## Requirements

* Python 3.7
* PyTorch > 1.0 

Installing the environment according to the README files in the ‘pose/openpose’ and 'music/madmom'.

## Music Process<a name="music-process"/>

```python
python music_process.py input_music_file -o output_path/filename.txt
```

For example:

```python
python music_process.py ./data/Jian_chrous.wav -o ./data/jian_beat.txt
```



##  Game Play<a name="game-play"/>

```
python play_game.py beat_file music_file [camera_id]
```

For example:

```
python play_game.py ./data/jian_beat.txt ./data/Jian_chrous.wav
```



## Citation:

If this helps your research, please cite the paper:

```
@inproceedings{osokin2018lightweight_openpose,
    author={Osokin, Daniil},
    title={Real-time 2D Multi-Person Pose Estimation on CPU: Lightweight OpenPose},
    booktitle = {arXiv preprint arXiv:1811.12004},
    year = {2018}
}
```

```
   @inproceedings{madmom,
      Title = {{madmom: a new Python Audio and Music Signal Processing Library}},
      Author = {B{\"o}ck, Sebastian and Korzeniowski, Filip and Schl{\"u}ter, Jan and Krebs, Florian and Widmer, Gerhard},
      Booktitle = {Proceedings of the 24th ACM International Conference on
      Multimedia},
      Month = {10},
      Year = {2016},
      Pages = {1174--1178},
      Address = {Amsterdam, The Netherlands},
      Doi = {10.1145/2964284.2973795}
   }
```

