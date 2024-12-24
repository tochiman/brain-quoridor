import React from 'react';
import { Button, Typography, Box } from '@mui/material';
import styles from '../styles/settingModal.module.css'; // CSSをインポート

interface RoomContentProps {
    roomName: string;
    userName: string;
}

const RoomContent: React.FC<RoomContentProps> = ({ roomName, userName }) => {
    // 降参ボタンを押したときの処理
    const handleSurrender = async () => {
        try {
            const response = await fetch('/api/surrender', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
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

    // ルーム退出ボタンを押したときの処理
    const handleLeaveRoom = async () => {
        try {
            const response = await fetch('/api/leave_room', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
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
            <Box mt={2}>
                <Button
                    variant="contained"
                    onClick={handleSurrender}
                    style={{ marginRight: '10px' }}
                >
                    降参
                </Button>
                <Button variant="contained" onClick={handleLeaveRoom}>
                    ルーム退出
                </Button>
            </Box>
        </Box>
    );
};

export default RoomContent;
