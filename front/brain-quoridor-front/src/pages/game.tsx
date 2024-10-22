import { Inter } from "next/font/google";
import styles from "@/styles/Home.module.css";
import { styled } from"@mui/material/styles";
import React, {HTMLAttributes, useState} from "react";
import { Grid, Paper, PaperProps, Typography } from "@mui/material";
import Head from "next/head";
import { light } from "@mui/material/styles/createPalette";


function range(start: number, end: number): number[] {
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
}

export default function Home() {
  const [hoveredRowId, setHoveredRowId] = useState<number>(0);
  const [hoveredColId, setHoveredColId] = useState<number>(0);
  const [hovered, setHovered] = useState<boolean>(false);
  const maxCol = 9;

  const handleMouseEnter = (bannmenRowId:number, bannmenColId:number) => {
    setHoveredRowId(bannmenRowId);
    setHoveredColId(bannmenColId);
    setHovered(true);
  };
  const handleMouseLeave = () => {
    setHoveredRowId(0);
    setHoveredColId(0);
    setHovered(false);
  }

  interface LightSpacingWallProps extends PaperProps  {
    bannmenRowId: number;
    bannmenColId: number;
  }
  interface StraightSpacingWallProps extends PaperProps  {
    bannmenRowId: number;
    bannmenColId: number;
  }

  // palette作った方がいいよ
  const LightSpacingWall = styled(Paper, {shouldForwardProp: (prop) => prop !== 'bannmenId',
  })<LightSpacingWallProps>(({ bannmenRowId, bannmenColId }) => ({
    backgroundColor: hovered && bannmenRowId === hoveredRowId &&  (bannmenColId === hoveredColId || bannmenColId === hoveredColId+1 ) 
    ? bannmenColId+1 <= 17 
    ? "#3c3c3c" : "#ffa5a5" : "#ffa5a5" ,
}))
const StraightSpacingWall = styled(Paper, {shouldForwardProp: (prop) => prop !== 'bannmenId',
})<StraightSpacingWallProps>(({ bannmenRowId, bannmenColId }) => ({
  backgroundColor: hovered && (bannmenRowId === hoveredRowId || bannmenRowId === hoveredRowId+2) && bannmenColId === hoveredColId ? "#3c3c3c" : "#ffa5a5",
}))

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
            <Grid container 
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
                        ? <Grid item   key={col}>
                            {/*横向き余白*/}
                            <div className={styles.banmeLightSpacing}>
                              <LightSpacingWall 
                              bannmenRowId={row}
                              bannmenColId={col}
                              className={styles.banmeLightSpacingScale}
                              onMouseEnter={() => handleMouseEnter(row, col)}
                              onMouseLeave={handleMouseLeave}
                              >
                              </LightSpacingWall>
                                {/* 交差点余白 */}
                              <Paper className={styles.banmeCrossSpacingScale}>
                              </Paper>
                            </div>
                          </Grid>
                        : <Grid item   key={col}>
                            {/*横向き余白*/}
                            <div className={styles.banmeLightSpacing}>
                              <LightSpacingWall 
                              bannmenRowId={row}
                              bannmenColId={col}
                              className={styles.banmeLightSpacingScale}
                              onMouseEnter={() => handleMouseEnter(row, col)}
                              onMouseLeave={handleMouseLeave}
                              >
                              </LightSpacingWall>
                            </div>
                          </Grid>
                      )
                    )))
                  : (range(1, 9).map((col) => (
                      ( col != 9
                        ? <Grid item   key={col}>
                            {/*盤目*/}
                            <div className={styles.banmeLightSpacing}>
                              <Paper className={styles.banmeScale}>
                              </Paper>
                                {/* 縦向き余白 */}
                              <StraightSpacingWall 
                              bannmenRowId={row}
                              bannmenColId={col}
                              className={styles.banmeStraightSpacingScale}
                              onMouseEnter={() => handleMouseEnter(row, col)}
                              onMouseLeave={handleMouseLeave}
                              >
                              </StraightSpacingWall>
                            </div>
                          </Grid>
                        : <Grid item   key={col}>
                            {/*盤目*/}
                            <div className={styles.banmeLightSpacing}>
                              <Paper className={styles.banmeScale}>
                              </Paper>
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