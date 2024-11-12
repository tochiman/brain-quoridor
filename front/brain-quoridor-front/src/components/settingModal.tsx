import React, { useState, useRef, useEffect } from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import Button from '@mui/material/Button';
import Select, { SelectChangeEvent } from '@mui/material/Select';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import InputLabel from '@mui/material/InputLabel';
import styles from '../styles/settingModal.module.css';

interface SettingModalProps {
  open: boolean;
  handleClose: () => void;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

// BGMオプションの定義
const bgmOptions = [
  { value: 'bgm1', label: 'エキサイティング', url: '/Yugioh.mp3' },
  { value: 'bgm2', label: 'リラックス', url: '/path/to/bgm2.mp3' },
  { value: 'bgm3', label: '集中', url: '/path/to/bgm3.mp3' },
  { value: 'none', label: 'BGMなし', url: '' },
];

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box className={styles.contentContainer}>
          <Typography component="div">{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const SettingModal: React.FC<SettingModalProps> = ({ open, handleClose }) => {
  const [value, setValue] = useState(0);
  const [selectedBGM, setSelectedBGM] = useState('none');
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const handleBGMChange = (event: SelectChangeEvent<string>) => {
    setSelectedBGM(event.target.value);
    setIsPlaying(false);
  };

  const handlePlayPause = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
      } else {
        audioRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const handleSaveBGM = () => {
    // Here you would implement the logic to save the selected BGM
    console.log('Saving BGM:', selectedBGM);
    alert('BGM設定を保存しました！');
  };

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.src = bgmOptions.find(option => option.value === selectedBGM)?.url || '';
      setIsPlaying(false);
    }
  }, [selectedBGM]);

  return (
    open && (
      <div className={styles.modalOverlay}>
        <div className={styles.modalContent}>
          <div className={styles.tabsAndCloseContainer}>
            <Tabs
              value={value}
              onChange={handleChange}
              aria-label="setting tabs"
              variant="fullWidth"
              className={styles.tabs}
            >
              <Tab label="ルーム" {...a11yProps(0)} />
              <Tab label="BGM" {...a11yProps(1)} />
              <Tab label="ルール" {...a11yProps(2)} />
            </Tabs>
            <IconButton
              aria-label="close"
              onClick={handleClose}
              className={styles.closeButton}
            >
              <CloseIcon />
            </IconButton>
          </div>

          <CustomTabPanel value={value} index={0}>
            <Typography style={{ color: '#333' }}>ルーム設定</Typography>
          </CustomTabPanel>
          <CustomTabPanel value={value} index={1}>
            <Typography variant="h6" gutterBottom>BGM設定</Typography>
            <FormControl fullWidth style={{ marginBottom: '20px' }}>
              <InputLabel id="bgm-select-label">BGMを選択</InputLabel>
              <Select
                labelId="bgm-select-label"
                id="bgm-select"
                value={selectedBGM}
                label="BGMを選択"
                onChange={handleBGMChange}
              >
                {bgmOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <div className={styles.bgmControls}>
              <Button
                variant="contained"
                onClick={handlePlayPause}
                disabled={selectedBGM === 'none'}
              >
                {isPlaying ? '停止' : '再生'}
              </Button>
              <Button
                variant="contained"
                onClick={handleSaveBGM}
                style={{ marginLeft: '10px' }}
              >
                BGM設定を保存
              </Button>
            </div>
            <audio ref={audioRef} />
          </CustomTabPanel>
          <CustomTabPanel value={value} index={2}>
            <Typography style={{ color: '#333' }}>ルール説明</Typography>
          </CustomTabPanel>
        </div>
      </div>
    )
  );
};

export default SettingModal;