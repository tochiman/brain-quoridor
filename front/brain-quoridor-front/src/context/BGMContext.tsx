// src/context/BGMContext.tsx
import React, { createContext, useState, useContext, ReactNode } from 'react';

interface BGMContextProps {
  playBGM: (url: string) => void;
  stopBGM: () => void;
}

const BGMContext = createContext<BGMContextProps | undefined>(undefined);

export const BGMProvider = ({ children }: { children: ReactNode }) => {
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  const playBGM = (url: string) => {
    if (audio) audio.pause(); // 既存のBGMを停止
    const newAudio = new Audio(url);
    newAudio.loop = true;
    newAudio.play();
    setAudio(newAudio);
  };

  const stopBGM = () => {
    if (audio) {
      audio.pause();
      setAudio(null);
    }
  };

  return (
    <BGMContext.Provider value={{ playBGM, stopBGM }}>
      {children}
    </BGMContext.Provider>
  );
};

export const useBGM = () => {
  const context = useContext(BGMContext);
  if (!context) {
    throw new Error('useBGM must be used within a BGMProvider');
  }
  return context;
};
