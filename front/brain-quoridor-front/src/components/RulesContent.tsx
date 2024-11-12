import React, { useState } from 'react';
import { Typography, Button, Dialog, DialogTitle, DialogContent } from '@mui/material';

function RulesContent() {
    const [openWallDialog, setOpenWallDialog] = useState(false);
    const [openMoveDialog, setOpenMoveDialog] = useState(false);

    const handleWallDialogOpen = () => setOpenWallDialog(true);
    const handleWallDialogClose = () => setOpenWallDialog(false);
    const handleMoveDialogOpen = () => setOpenMoveDialog(true);
    const handleMoveDialogClose = () => setOpenMoveDialog(false);

    return (
        <div>
            <Typography variant="h6">勝利条件</Typography>
            <Typography>自分のコマを相手側の陣地に到達させること。</Typography>

            <Typography variant="h6" style={{ marginTop: '20px' }}>壁の枚数</Typography>
            <Typography>各プレイヤーに10枚。</Typography>

            <Typography variant="h6" style={{ marginTop: '20px' }}>ゲームの説明</Typography>
            <Typography>壁で相手の進路を妨害しながら、自分のコマを相手陣地に進めましょう！</Typography>

            <div style={{ marginTop: '20px' }}>
                <Button variant="outlined" onClick={handleWallDialogOpen}>
                    壁の置き方
                </Button>
                <Button variant="outlined" onClick={handleMoveDialogOpen} style={{ marginLeft: '10px' }}>
                    コマの動かし方
                </Button>
            </div>

            {/* 壁の置き方ダイアログ */}
            <Dialog open={openWallDialog} onClose={handleWallDialogClose}>
                <DialogTitle>壁の置き方</DialogTitle>
                <DialogContent>
                    <Typography>
                        壁はプレイヤーの進路を塞ぐために置くことができます。壁はコマの進路に対して垂直または水平に配置できます。
                    </Typography>
                </DialogContent>
            </Dialog>

            {/* コマの動かし方ダイアログ */}
            <Dialog open={openMoveDialog} onClose={handleMoveDialogClose}>
                <DialogTitle>コマの動かし方</DialogTitle>
                <DialogContent>
                    <Typography>
                        コマは一度に一マス移動できます。隣接するマスに移動するか、相手のコマを飛び越えることもできます。
                    </Typography>
                </DialogContent>
            </Dialog>
        </div>
    );
}

export default RulesContent;
