import React, { useState } from 'react';
import { Typography, Card, CardContent, Button, Grid, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';

interface RulesContentProps { }

const RulesContent: React.FC<RulesContentProps> = () => {
    const [dialogOpen, setDialogOpen] = useState<string | null>(null);

    const handleDialogOpen = (type: string) => {
        setDialogOpen(type);
    };

    const handleDialogClose = () => {
        setDialogOpen(null);
    };

    return (
        <>
            <Grid container spacing={2} direction="column">
                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" style={{ fontWeight: 'bold', color: '#333' }}>
                                ゲームの目的
                            </Typography>
                            <Typography style={{ color: '#555' }}>
                                自分のコマを相手側のゴールラインまで移動させることが目的です。
                            </Typography>
                            <Button variant="outlined" onClick={() => handleDialogOpen("move")} style={{ marginTop: '10px' }}>
                                詳細を見る
                            </Button>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" style={{ fontWeight: 'bold', color: '#333' }}>
                                コマの動かし方
                            </Typography>
                            <Typography style={{ color: '#555' }}>
                                コマは上下左右に1マス移動します。相手のコマを飛び越えることも可能です。
                            </Typography>
                            <Button variant="outlined" onClick={() => handleDialogOpen("move")} style={{ marginTop: '10px' }}>
                                詳細を見る
                            </Button>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12}>
                    <Card>
                        <CardContent>
                            <Typography variant="h6" style={{ fontWeight: 'bold', color: '#333' }}>
                                壁の使用
                            </Typography>
                            <Typography style={{ color: '#555' }}>
                                各プレイヤーは10枚の壁を使って相手の進路を妨害できます。
                            </Typography>
                            <Button variant="outlined" onClick={() => handleDialogOpen("wall")} style={{ marginTop: '10px' }}>
                                詳細を見る
                            </Button>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* ダイアログ表示部分 */}
            <Dialog open={dialogOpen !== null} onClose={handleDialogClose} maxWidth="sm" fullWidth>
                <DialogTitle>
                    {dialogOpen === "purpose" ? "勝利条件" : dialogOpen === "move" ? "コマの動かし方" : dialogOpen === "wall" ? "壁の置き方" : ""}
                </DialogTitle>
                <DialogContent>
                    {dialogOpen === "purpose" && (
                        <>
                            <Typography style={{ color: '#333', marginBottom: '16px' }}>
                                壁を駆使しながら相手側の最終ラインまで進みましょう
                            </Typography>
                            <img
                                src="/assets/gifs/sample.gif"
                                alt="勝利条件"
                                style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
                            />
                        </>
                    )}
                    {dialogOpen === "move" && (
                        <>
                            <Typography style={{ color: '#333', marginBottom: '16px' }}>
                                コマは上下左右に1マスずつ動かすことができます。また、相手のコマを飛び越えることも可能です。
                            </Typography>
                            <img
                                src="/assets/gifs/sample.gif"
                                alt="コマの動かし方の例"
                                style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
                            />
                        </>
                    )}
                    {dialogOpen === "wall" && (
                        <>
                            <Typography style={{ color: '#333', marginBottom: '16px' }}>
                                壁を縦か横に置いて、相手の進路を妨害できます。ただし、完全に道を塞ぐことはできません。
                            </Typography>
                            <img
                                src="/assets/gifs/sample.gif"
                                alt="壁の置き方の例"
                                style={{ width: '100%', height: 'auto', borderRadius: '8px' }}
                            />
                        </>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleDialogClose} color="primary">
                        閉じる
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
};

export default RulesContent;
