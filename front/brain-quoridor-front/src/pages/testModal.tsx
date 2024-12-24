import React, { useState, useRef } from 'react';
import Button from '@mui/material/Button';
import SettingModal from '../components/settingModal';

export default function TestModal() {
  const [open, setOpen] = useState(false);
  const [selectedBGM, setSelectedBGM] = useState('none'); // 現在選択されているBGM
  const audioRef = useRef<HTMLAudioElement | null>(null); // 音楽再生用のref
  const [isPlaying, setIsPlaying] = useState(false); // 再生状態

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  // 音楽再生の関数
  const handlePlayBGM = (url: string) => {
    if (audioRef.current) {
      audioRef.current.src = url; // 再生する音楽のURLを設定
      audioRef.current.play(); // 再生開始
      setIsPlaying(true);
    }
  };

  // 音楽停止の関数
  const handlePauseBGM = () => {
    if (audioRef.current) {
      audioRef.current.pause(); // 再生停止
      setIsPlaying(false);
    }
  };

  // BGM選択時の処理
  const handleBGMChange = (newValue: string) => {
    setSelectedBGM(newValue);
  };

  return (
    <div>
      <Button variant="contained" onClick={handleOpen}>
        設定を開く
      </Button>
      <audio ref={audioRef} /> {/* オーディオ要素 */}
      <SettingModal
        open={open}
        handleClose={handleClose}
        selectedBGM={selectedBGM}
        onBGMChange={handleBGMChange}
        handlePlayBGM={handlePlayBGM}
        handlePauseBGM={handlePauseBGM}
        isPlaying={isPlaying}
      />
    </div>
  );
}
