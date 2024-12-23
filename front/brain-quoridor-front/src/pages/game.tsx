import styles from "@/styles/Home.module.css";
import { styled } from"@mui/material/styles";
import React, {HTMLAttributes, useState, useEffect, useRef} from "react";
import { Grid, ListClassKey, Paper, PaperProps, Typography } from "@mui/material";
import Head from "next/head";

function range(start: number, end: number): number[] {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}

export default function Home() {  //useStateの宣言 ホバーの真偽宣言
  const [hoveredrowid, setHoveredrowid] = useState<number>(0);
  const [hoveredcolid, setHoveredcolid] = useState<number>(0);
  const [hoverednextcolid, setHoverednextcolid] = useState<number>(0);
  const [hoverednextrowid, setHoverednextrowid] = useState<number>(0);
  const [hovered, setHovered] = useState<boolean>(false);
  const [receiveddata, setreceiveddata] = useState<any>();
  const [currentrowid, setcurrentrowid] = useState<number>(0);
  const [currentcolid, setcurrentcolid] = useState<number>(0);

  const handleMouseEnter = (bannmenrowid:number, bannmencolid:number, nextbannmencolid:number, nextbannmenrowid: number) => {
    setHoveredrowid(bannmenrowid);
    setHoveredcolid(bannmencolid);
    setHoverednextcolid(nextbannmencolid);
    setHoverednextcolid(nextbannmenrowid);
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
    setHoverednextcolid(0);
    setHoverednextrowid(0);
    setHovered(false);
  }

  interface WebSocketData {
      "name": string
      "other_name": string
      "turn": boolean
      "position": number
      "other_position": number
      "wall": number
      "other_wall": number
      "color": string
      "move_list": number
      "board": any
      "item_position": number
      "item": any
      "other_item": any
  }
  interface BanmeProps extends PaperProps {
    receiveddata: any;
    currentrowid: number;
    currentcolid: number;
  }
  interface LightSpacingWallProps extends PaperProps  {
    bannmenrowid: number;
    bannmencolid: number;
    nextbannmencolid: number;
    nextbannmenrowid: number;
  }
  interface StraightSpacingWallProps extends PaperProps  {
    bannmenrowid: number;
    bannmencolid: number;
    nextbannmencolid: number;
    nextbannmenrowid: number;
  }

  // palette作った方がいいよ
  const LightSpacingWall = styled(Paper, {shouldForwardProp: (prop) => prop !== 'bannmenid',
  })<LightSpacingWallProps>(({ bannmenrowid, bannmencolid }) => ({
    backgroundColor: hovered && bannmenrowid === hoveredrowid &&  (bannmencolid === hoveredcolid || bannmencolid === hoveredcolid+1 ) 
    ? "rgba(102, 102, 102, 0.5)" : "rgb(44, 26, 1)"  ,
    transition: 'background-color 9ms',
    transitionDelay: '9ms',
}))
  const StraightSpacingWall = styled(Paper, {shouldForwardProp: (prop) => prop !== 'bannmenid',
  })<StraightSpacingWallProps>(({ bannmenrowid, bannmencolid }) => ({
    backgroundColor: hovered && (bannmenrowid === hoveredrowid || bannmenrowid === hoveredrowid+2) && bannmencolid === hoveredcolid 
    ? "rgba(102, 102, 102, 0.5)" : "rgb(44, 26, 1)",
    transition: 'background-color 9ms',
    transitionDelay: '9ms',
}))
  const Banme = styled(Paper, {shouldForwardProp: (prop) => prop !== 'bannmenid',
  })<BanmeProps>(({ receiveddata, currentrowid, currentcolid }) => ({
    backgroundColor: (receiveddata?.position?.[0] === currentcolid-1 && receiveddata?.position?.[1] === currentrowid-1) ? "rgb(0, 0, 0)" : "rgb(235, 141, 11)"
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
      console.log(response.json())
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
      setreceiveddata(JSON.parse(event.data))
      console.log(JSON.parse(event.data))
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
                              <LightSpacingWall 
                              bannmenrowid={row}
                              bannmencolid={col}
                              nextbannmencolid={col+1}
                              nextbannmenrowid={row}
                              className={styles.banmeLightSpacingScale}
                              onMouseEnter={() => handleMouseEnter(row, col, col+1, row)}
                              onMouseLeave={handleMouseLeave}
                              >
                              </LightSpacingWall>
                                {/* 交差点余白 */}
                              <Paper className={styles.banmeCrossSpacingScale}>
                              </Paper>
                            </div>
                          </Grid>
                        : <Grid item key={col}>
                            {/*横向き余白*/}
                            <div className={styles.banmeLightSpacing}>
                              <LightSpacingWall 
                              bannmenrowid={row}
                              bannmencolid={col}
                              nextbannmencolid={col+1}
                              nextbannmenrowid={row}
                              className={styles.banmeLightSpacingScale}
                              onMouseEnter={() => handleMouseEnter(row, col, col+1, row)}
                              onMouseLeave={handleMouseLeave}
                              >
                              </LightSpacingWall>
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
                                receiveddata={receiveddata} 
                                currentrowid={row}
                                currentcolid={col}>
                                </Banme>
                              </div>
                                {/* 縦向き余白 */}
                              <StraightSpacingWall 
                              bannmenrowid={row}
                              bannmencolid={col}
                              nextbannmencolid={col}
                              nextbannmenrowid={row+2}
                              className={styles.banmeStraightSpacingScale}
                              onMouseEnter={() => handleMouseEnter(row, col, col, row+2)}
                              onMouseLeave={handleMouseLeave}>
                              </StraightSpacingWall>
                            </div>
                          </Grid>
                        : <Grid item key={col}>
                            {/*盤目*/}
                            <div className={styles.banmeLightSpacing}>
                              <div onClick={() => piece_move(col, row)}>
                              <Banme
                                className={styles.banmeScale}
                                receiveddata={receiveddata} 
                                currentrowid={row}
                                currentcolid={col}>
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
        </main>
      </>
    );
  }