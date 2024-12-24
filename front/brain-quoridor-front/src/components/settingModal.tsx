import React, { useState } from 'react';
import Box from '@mui/material/Box';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import BGMContent from './BGMContent';
import RulesContent from './RulesContent';
import RoomContent from './RoomContent';
import styles from '../styles/settingModal.module.css';

interface SettingModalProps {
  open: boolean;
  handleClose: () => void;
  selectedBGM: string;
  onBGMChange: (newValue: string) => void;
  handlePlayBGM: (url: string) => void;
  handlePauseBGM: () => void;
  isPlaying: boolean;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
      className={styles.tabPanel}
    >
      {value === index && <Box className={styles.contentContainer}>{children}</Box>}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

const SettingModal: React.FC<SettingModalProps> = ({
  open,
  handleClose,
  selectedBGM,
  onBGMChange,
  handlePlayBGM,
  handlePauseBGM,
  isPlaying,
}) => {
  const [value, setValue] = useState(0); // 初期タブ設定

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

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
            <RoomContent />
          </CustomTabPanel>

          <CustomTabPanel value={value} index={1}>
            <BGMContent
              selectedBGM={selectedBGM}
              onBGMChange={onBGMChange}
              handlePlayBGM={handlePlayBGM}
              handlePauseBGM={handlePauseBGM}
              isPlaying={isPlaying}
            />
          </CustomTabPanel>

          <CustomTabPanel value={value} index={2}>
            <RulesContent />
          </CustomTabPanel>
        </div>
      </div>
    )
  );
};

export default SettingModal;
