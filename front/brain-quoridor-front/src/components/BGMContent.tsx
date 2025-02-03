import React, { useState } from 'react';

interface BGMContentProps {
    selectedBGM: string;
    onBGMChange: (newValue: string) => void;
    isPlaying: boolean;
    handlePlayBGM: (url: string) => void;
    handlePauseBGM: () => void;
}

const BGMContent: React.FC<BGMContentProps> = ({
    selectedBGM,
    onBGMChange,
    isPlaying,
    handlePlayBGM,
    handlePauseBGM,
}) => {
    const bgmOptions = [
        { value: 'bgm1', label: 'エキサイティング', url: '/assets/bgm/Yugioh.mp3' },
        { value: 'bgm2', label: 'リラックス', url: '/assets/bgm/bgm2.mp3' },
        { value: 'none', label: 'BGMなし', url: '' },
    ];

    // 音楽変更時の処理
    const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const newValue = event.target.value;
        onBGMChange(newValue);

        const selectedOption = bgmOptions.find((option) => option.value === newValue);
        if (selectedOption && selectedOption.url) {
            handlePlayBGM(selectedOption.url);
        } else {
            handlePauseBGM();
        }
    };

    return (
        <div>
            <h3>🎵 BGM設定</h3>
            <select value={selectedBGM} onChange={handleChange}>
                {bgmOptions.map((option) => (
                    <option key={option.value} value={option.value}>
                        {option.label}
                    </option>
                ))}
            </select>
            <div style={{ marginTop: '10px' }}>
                <button onClick={isPlaying ? handlePauseBGM : () => handlePlayBGM(bgmOptions.find(o => o.value === selectedBGM)?.url || '')}>
                    {isPlaying ? '⏸ 停止' : '▶️ 再生'}
                </button>
            </div>
        </div>
    );
};

export default BGMContent;
