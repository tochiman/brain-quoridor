import styles from "@/styles/Home.module.css";
import { styled } from"@mui/material/styles";
import React, {HTMLAttributes, useState, useEffect, useRef} from "react";
import { Grid, ListClassKey, Paper, PaperProps, Typography, Button, stepLabelClasses } from "@mui/material";
import Head from "next/head";
import { ConstructionOutlined } from "@mui/icons-material";
import SettingModal from '../components/settingModal';

function range(start: number, end: number): number[] {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}

export default function Home() {  //useStateの宣言 ホバーの真偽宣言
  const [hoveredrowid, setHoveredrowid] = useState<number>(0);
  const [hoveredcolid, setHoveredcolid] = useState<number>(0);
  const [hovered, setHovered] = useState<boolean>(false);
  const [receiveddata, setreceiveddata] = useState<any>();
  const [wall, setwall] = useState<any>([]);
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
  

  const handleMouseEnter = (bannmenrowid:number, bannmencolid:number, nextbannmencolid:number, nextbannmenrowid: number) => {
    setHoveredrowid(bannmenrowid);
    setHoveredcolid(bannmencolid);
    if (nextbannmencolid==10){
      setHoveredcolid(-1); //端が光らないように
    }
    if (nextbannmenrowid==19){
      setHoveredrowid(0); //端が光らないように
    }
    setHovered(true);
  };
  const handleMouseLeave = () => {
    setHoveredrowid(0);
    setHoveredcolid(0);
    setHovered(false);
  }

  interface WebSocketData {
      "turn": boolean
      "position": number
      "other_position": number
      "wall": number
      "other_wall": number
      "color": string
      "move_list": any
      "board": any
      "item_position": number
      "item": any
      "other_item": any
  }
  interface BanmeProps extends PaperProps {
    backgroundcolor: string;
  }
  interface LightSpacingWallProps extends PaperProps  {
    backgroundcolor: string;
  }
  interface StraightSpacingWallProps extends PaperProps  {
    backgroundcolor: string;
  }

  // palette作った方がいいよ
  const LightSpacingWall = styled(Paper, {shouldForwardProp: (prop) => prop !== 'bannmenid',
  })<LightSpacingWallProps>(({ backgroundcolor }) => ({
    backgroundColor: backgroundcolor
}))
  const StraightSpacingWall = styled(Paper, {shouldForwardProp: (prop) => prop !== 'bannmenid',
  })<StraightSpacingWallProps>(({ backgroundcolor }) => ({
    backgroundColor: backgroundcolor
}))
  const Banme = styled(Paper, {shouldForwardProp: (prop) => prop !== 'bannmenid',
  })<BanmeProps>(({ backgroundcolor }) => ({
    backgroundColor: backgroundcolor
}))


function piece_move (x:number, y:number) {
  // rowが縦積みで17行ある為、9行に直すための処理
  if (y !== 1) {
    let tmp = y
    let i
    for (i=0; tmp>1; i++){
      tmp-=2
    }
    y = y-i
  }
  x=x-1
  y=y-1

  // postData更新
  const postData = {
    x: x,
    y: y,
  };

  fetch('/api/move', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(postData),
  })
    .then(response => {
      if (response.status === 200){
        console.log("sucsses")
      }else if (response.status === 400){
        console.log("failed")
      }
    }
  )
    .catch(error => {
      console.error('Error:', error);
    });
}

function piece_wall(x:number, y:number, type:string) {

    // rowが縦積みで17行ある為、9行に直すための処理
    if (y !== 1) {
      let tmp = y
      let i
      for (i=0; tmp>1; i++){
        tmp-=2
      }
      y = y-i
    }

    x=x-1
    y=y-1

  //postData更新
  const postData = {
      x: x,
      y: y,
      wall_type: type
  };
  fetch(`/api/wall`, {
      method: 'POST',
      headers: {
          "Content-Type": 'application/json'
      },
      body: JSON.stringify(postData)
  })
  .then(response => {
    if (response.status === 200){
      console.log("sucsses")
    }else if (response.status === 400){
      console.log("failed")
    }
  }
)
  .catch(error => {
    console.error('Error:', error);
  });
}


//Websocketの呼び出し
const socketRef = useRef<WebSocket>()
const [isConnected, setIsConnected] = useState<boolean>(false)

useEffect(() => {

  socketRef.current = new WebSocket("/api/ws")
    socketRef.current.onopen = function () {
      setIsConnected(true)
      console.log('Connected')
    }

    socketRef.current.onclose = function () {
      setIsConnected(false)
      console.log('closed')
    }

    socketRef.current.onmessage = function (event) {
      const socketdata=JSON.parse(event.data)
      if (socketdata.message !== "pong") {
        setreceiveddata(socketdata)
        console.log(socketdata)
      }
    }
},[]

)
    return (
      <>
        <Head>
          <title>Quoridor</title>
          <meta name="description" content="Generated by create next app" />
          <meta name="viewport" content="width=device-width, initial-scale=1" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        <main>
        <div >
        <Button className={styles.Optionbtn} variant="contained" onClick={handleOpen}>
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

        <Paper className={styles.itemview}>
          所持アイテム：
          {receiveddata?.item
            ?.map((item:any) => {
              if (item === "break_wall") return "壁破壊";
              if (item === "twice") return "二回行動";
              if (item === "free_wall") return "壁設置";
              return item; 
            })
            .join("、 ")}
        </Paper>
        <div className={styles.verticalgrid}>
        <Paper className={styles.holdwalltop}>相手 残りの壁：{receiveddata?.other_wall}枚</Paper>
          <Paper className={styles.dodai}>
            <Grid container item
              className={`${styles.relativeScale} ${styles.gridField}`}             
            >
              {range(1, 17).map((row) => (
                <Grid container item
                  className={styles.banmenCenter}
                  key={row}
                >
                  {row % 2 === 0 
                  ? (range(1, 9).map((col) => (
                      ( col != 9
                        ? <Grid item key={col}>
                            {/*横向き余白*/}
                            <div className={styles.banmeLightSpacing}>
                              <div onClick={() => piece_wall(col, row, "h")}>
                                <LightSpacingWall 
                                className={styles.banmeLightSpacingScale}
                                onMouseEnter={() => handleMouseEnter(row, col, col+1, row)}
                                onMouseLeave={handleMouseLeave}
                                backgroundcolor={
                                  (() => {
                                      if (hovered && row === hoveredrowid &&  (col === hoveredcolid || col === hoveredcolid+1 )){
                                        return "rgba(102, 102, 102, 0.5)"
                                      } else{
                                      for (let i:number=0; i<receiveddata?.board?.length; i++){
                                        if(((receiveddata?.board[i][0] === col-1) || (receiveddata?.board[i][0] === col-2)) && (((receiveddata?.board[i][1])*2) === row-2) && (receiveddata?.board[i][2] === "h")){
                                            return "rgb(248, 0, 215)"
                                          }
                                        }
                                      return "rgb(44, 26, 1)"
                                      }
                                    }
                                  )()
                                }
                                >
                                </LightSpacingWall>
                              </div>
                                {/* 交差点余白 */}
                              <Paper className={styles.banmeCrossSpacingScale}>
                              </Paper>
                            </div>
                          </Grid>
                        : <Grid item key={col}>
                            {/*横向き余白*/}
                            <div className={styles.banmeLightSpacing}>
                              <div onClick={() => piece_wall(col, row, "h")}>
                                <LightSpacingWall 
                                className={styles.banmeLightSpacingScale}
                                onMouseEnter={() => handleMouseEnter(row, col, col+1, row)}
                                onMouseLeave={handleMouseLeave}
                                backgroundcolor={
                                  (() => {
                                      if (hovered && row === hoveredrowid &&  (col === hoveredcolid || col === hoveredcolid+1 )){
                                        return "rgba(102, 102, 102, 0.5)"
                                      } else{
                                      for (let i:number=0; i<receiveddata?.board?.length; i++){
                                        if(((receiveddata?.board[i][0] === col-1) || (receiveddata?.board[i][0] === col-2)) && (((receiveddata?.board[i][1])*2) === row-2) && (receiveddata?.board[i][2] === "h")){
                                            return "rgb(248, 0, 215)"
                                          }
                                        }
                                      return "rgb(44, 26, 1)"
                                      }
                                    }
                                  )()
                                }
                                >
                                </LightSpacingWall>
                              </div>
                            </div>
                          </Grid>
                      )
                    )))
                  : (range(1, 9).map((col) => (
                      ( col != 9
                        ? <Grid item key={col}>
                            {/*盤目*/}
                            <div className={styles.banmeLightSpacing}>
                              <div onClick={() => piece_move(col, row)}>
                                <Banme
                                className={styles.banmeScale}
                                backgroundcolor={
                                  (() =>{
                                      if ((receiveddata?.position?.[0] === col-1) && (((receiveddata?.position?.[1])*2) === row-1)){
                                        if (receiveddata?.color === "b")
                                          return "rgb(0,0,0)"
                                        else
                                          return "rgb(255,255,255)"
                                      }
                                      else if ((receiveddata?.other_position?.[0] === col-1) && (((receiveddata?.other_position?.[1])*2) === row-1)){
                                        if (receiveddata?.color === "b")
                                          return "rgb(255, 255, 255)"
                                        else
                                          return "rgb(0, 0, 0)"
                                      }
                                      else{
                                        let canmove:any = []
                                        for (let i:number=0; i<receiveddata?.move_list?.length; i++){
                                          if (receiveddata?.move_list?.[i][0] === "move")
                                            canmove.push(receiveddata?.move_list?.[i])
                                        }
                                        for (let i:number=0; i<canmove.length; i++){
                                          if((canmove[i][1] === col-1) && (((canmove[i][2])*2) === row-1)){
                                            if (receiveddata?.color === "b")
                                              return "rgba(55, 55, 55, 0.8)"
                                            else
                                            return "rgba(200, 200, 200, 0.4)"
                                          }
                                        }
                                        for (let i:number=0; i<receiveddata?.item_position?.length; i++){
                                          if ((receiveddata?.item_position?.[i][0] === col-1) && (((receiveddata?.item_position?.[i][1])*2) === row-1)){
                                            return "rgb(53, 168, 7)"
                                          }
                                        }
                                        return "rgb(190, 117, 13)"
                                      }
                                  })()
                                }
                                >
                                </Banme>
                              </div>
                                {/* 縦向き余白 */}
                              <div onClick={() => piece_wall(col, row, "v")}>
                                <StraightSpacingWall 
                                className={styles.banmeStraightSpacingScale}
                                onMouseEnter={() => handleMouseEnter(row, col, col, row+2)}
                                onMouseLeave={handleMouseLeave}
                                backgroundcolor={
                                  (() => {
                                      if (hovered && (row === hoveredrowid || row === hoveredrowid+2) && col === hoveredcolid){
                                        return "rgba(102, 102, 102, 0.5)"
                                    } else{
                                      for (let i:number=0; i<receiveddata?.board?.length; i++){
                                        if((receiveddata?.board[i][0] === col-1) && ((((receiveddata?.board[i][1])*2) === row-1) || (((receiveddata?.board[i][1])*2) === row-3)) && (receiveddata?.board[i][2] === "v")){
                                            return "rgb(248, 0, 215)"
                                          }
                                        }
                                      return "rgb(44, 26, 1)"
                                      }
                                    }
                                  )()
                                }
                                >
                                </StraightSpacingWall>
                              </div>
                            </div>
                          </Grid>
                        : <Grid item key={col}>
                            {/*盤目*/}
                            <div className={styles.banmeLightSpacing}>
                              <div onClick={() => piece_move(col, row)}>
                              <Banme
                                className={styles.banmeScale}
                                backgroundcolor={
                                  (() =>{
                                      if ((receiveddata?.position?.[0] === col-1) && (((receiveddata?.position?.[1])*2) === row-1)){
                                        if (receiveddata?.color === "b")
                                          return "rgb(0,0,0)"
                                        else
                                          return "rgb(255,255,255)"
                                      }
                                      else if ((receiveddata?.other_position?.[0] === col-1) && (((receiveddata?.other_position?.[1])*2) === row-1)){
                                        if (receiveddata?.color === "b")
                                          return "rgb(255, 255, 255)"
                                        else
                                          return "rgb(0, 0, 0)"
                                      }
                                      else{
                                        let canmove:any = []
                                        for (let i:number=0; i<4; i++){
                                          if (receiveddata?.move_list?.[i][0] === "move")
                                            canmove.push(receiveddata?.move_list?.[i])
                                        }
                                        for (let i:number=0; i<canmove.length; i++){
                                          if((canmove[i][1] === col-1) && (((canmove[i][2])*2) === row-1)){
                                            if (receiveddata?.color === "b")
                                              return "rgba(55, 55, 55, 0.8)"
                                            else
                                            return "rgba(200, 200, 200, 0.4)"
                                          }
                                        }
                                        return "rgb(190, 117, 13)"
                                      }
                                  })()
                                }>
                              </Banme>
                              </div>
                            </div>
                          </Grid>
                      )
                    )))
                  }
                </Grid>
              ))}
            </Grid>
          </Paper>
          <Paper className={styles.holdwallbottom}>自分 残りの壁：{receiveddata?.wall}枚</Paper>
          </div>
        </main>
      </>
    );
  }