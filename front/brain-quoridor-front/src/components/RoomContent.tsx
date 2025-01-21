import React, { useEffect, useState } from 'react';
import { Button, Typography, Box } from '@mui/material';
import styles from '../styles/settingModal.module.css'; // CSSをインポート

const RoomContent: React.FC = () => {
    const [roomName, setRoomName] = useState('');
    const [userName, setUserName] = useState('');
    const [otherName, setOtherName] = useState('');

    // ルーム情報を取得
    const fetchRoomInfo = async () => {
        try {
            const response = await fetch('/api/info', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include', // クッキーを送信する
            });

            if (response.ok) {
                const data = await response.json();
                setRoomName(data.room_name);
                setUserName(data.name);
                setOtherName(data.other_name);
            } else {
                const errorData = await response.json();
                alert(`エラー: ${errorData.message}`);
            }
        } catch (error) {
            console.error('Network Error:', error);
            alert('ネットワークエラーが発生しました');
        }
    };

    // コンポーネント初期化時に情報を取得
    useEffect(() => {
        fetchRoomInfo();
    }, []);

    // 降参ボタンを押したときの処理
    const handleSurrender = async () => {
        try {
            const response = await fetch('/api/surrender', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            });

            if (response.ok) {
                const data = await response.json();
                alert(data.message); // 成功メッセージを表示
            } else {
                const errorData = await response.json();
                alert(`エラー: ${errorData.message}`); // エラーメッセージを表示
            }
        } catch (error) {
            console.error('Network Error:', error);
            alert('ネットワークエラーが発生しました');
        }
    };

    return (
        <Box>
            <Typography variant="h6" className={styles.roomInfo}>
                ルーム情報
            </Typography>
            <Typography className={styles.roomInfo}>
                ルーム名: {roomName}
            </Typography>
            <Typography className={styles.roomInfo}>
                ユーザー名: {userName}
            </Typography>
            <Typography className={styles.roomInfo}>
                相手の名前: {otherName}
            </Typography>
            <Box mt={2}>
                <Button
                    variant="contained"
                    onClick={handleSurrender}
                    style={{ marginRight: '10px' }}
                >
                    降参
                </Button>
            </Box>
        </Box>
    );
};

export default RoomContent;
