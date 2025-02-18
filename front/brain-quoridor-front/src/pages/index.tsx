import Head from "next/head";
import { Inter } from "next/font/google";
import styles from "@/styles/Home.module.css";
import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import TextField from '@mui/material/TextField';
import CloseIcon from '@mui/icons-material/Close';
import { rulesContent } from '../styles/rule.js';
import { rules_itemContent } from '../styles/rule_item.js';
import { useForm } from "react-hook-form";
import Router from 'next/router';
//import styles from "@/styles/start.module.css"


const inter = Inter({ subsets: ["latin"] });

const styleModal = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 500,
  height: '310px',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
};

const styleRuleModal = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: "70%",
  height: '70%',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  overflow: "scroll",
};

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function CustomTabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

interface RoomData {
  roomName: string;
  userName: string;
  action: 'create' | 'join';
}

function taisen_ai (){
  fetch('/api/ai', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
  })
  .then(response => {
    if (response.status === 200){
      Router.push('/game');
    }else if (response.status === 400){
      console.log("failed")
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

export default function main() {
  const { register, handleSubmit, formState: { isValid } } = useForm<RoomData>({
    mode: "onChange"
  });

  const [openBattleModal, setOpenBattleModal] = React.useState(false);
  const [openRuleModal, setOpenRuleModal] = React.useState(false);
  const [value, setValue] = React.useState(0);
  const [lockButton, setLockButton] = React.useState(false);

  const handleOpenBattleModal = () => setOpenBattleModal(true);
  const handleCloseBattleModal = () => setOpenBattleModal(false);
  const handleOpenRuleModal = () => setOpenRuleModal(true);
  const handleCloseRuleModal = () => setOpenRuleModal(false);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const onSubmit = (data: RoomData) => {
    setLockButton(true);
    if (data.action === 'create') {
      createRoom(data);
    } else {
      joinRoom(data);
    }
  };

  const createRoom = (data: RoomData) => {
    const postData = { room_name: data.roomName, user_name: data.userName };
    fetch('/api/create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData),
    })
    .then(response => {
      if (response.status === 200) {
        Router.push('/game');
      } else if (response.status === 400) {
        alert('既に存在します');
      }
      setLockButton(false);
    })
    .catch(error => {
      console.error('Error:', error);
      setLockButton(false);
    });
  };

  const joinRoom = (data: RoomData) => {
    const postData = { room_name: data.roomName, user_name: data.userName };
    fetch('/api/join', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(postData),
    })
    .then(response => {
      if (response.status === 200) {
        Router.push('/game');
      } else if (response.status === 400) {
        alert('参加できませんでした');
      }
      setLockButton(false);
    })
    .catch(error => {
      console.error('Error:', error);
      setLockButton(false);
    });
  };

  return (
    <>
      <Head>
        <title>Create</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={`${styles.main} ${inter.className}`}>
        <h1>Brain Quoridall</h1>
        <div className="button-container">
          <Button onClick={handleOpenBattleModal}>知恵比べ</Button>
          <Modal
            open={openBattleModal}
            onClose={handleCloseBattleModal}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
          >
            <Box sx={styleModal} pt={2} pb={"330px"} pl={2} pr={2}>
              <Box onClick={handleCloseBattleModal} sx={{textAlign:"right"}}>
                <CloseIcon></CloseIcon>
              </Box>
              <Typography id="modal-modal-title" variant="h6" component="h2">
                <Box sx={{ width: '100%' }}>
                  <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                    <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                      <Tab label="対戦" {...a11yProps(0)} />
                      <Tab label="AI" {...a11yProps(1)} />
                    </Tabs>
                  </Box>
                  <CustomTabPanel value={value} index={0}>
                    <form onSubmit={handleSubmit(onSubmit)}>
                      <Box sx={{ '& > :not(style)': { m: 1, width: '25ch' } }}>
                        <TextField {...register("roomName", { required: true, maxLength: {value: 15, message: "15文字までです"}})} label="ルーム名" variant="outlined" type="text" inputProps={{ maxLength: 15 }}/>
                        <TextField {...register("userName", { required: true, maxLength: {value: 15, message: "15文字までです"}})} label="ユーザー名" variant="outlined" type="text" inputProps={{ maxLength: 15 }}/>
                      </Box>
                      <Button onClick={() => handleSubmit((data) => onSubmit({ ...data, action: 'create' }))()} disabled={!isValid || lockButton}>
                        作成
                      </Button>
                      <Button onClick={() => handleSubmit((data) => onSubmit({ ...data, action: 'join' }))()} disabled={!isValid || lockButton}>
                        参加
                      </Button>
                    </form>
                  </CustomTabPanel>

                  <CustomTabPanel value={value} index={1}>
                    <Box
                        component="form"
                        sx={{
                          '& > :not(style)': { m: 1, width: '25ch' },
                        }}
                        noValidate
                        autoComplete="off"
                    >                        
                    </Box>
                    <Button onClick={() => taisen_ai()}>対戦</Button>
                  </CustomTabPanel>

                </Box>
              </Typography>
            </Box>
          </Modal>
        </div>
        <Button onClick={handleOpenRuleModal}>ルール</Button>
        <Modal
          open={openRuleModal}
          onClose={handleCloseRuleModal}
          aria-labelledby="modal-modal-title"
          aria-describedby="modal-modal-description"
        >
          <Box sx={styleRuleModal} pt={2} pb={"330px"} pl={2} pr={2}>
            <Box onClick={handleCloseRuleModal} sx={{textAlign:"right"}}>
              <CloseIcon></CloseIcon>
            </Box>
            <Typography id="modal-modal-title" variant="h6" component="h2">
              <Box sx={{ width: '100%' }}>
                <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
                  <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
                    <Tab label="基本" {...a11yProps(0)} />
                    <Tab label="アイテム" {...a11yProps(1)} />
                  </Tabs>
                </Box>
                <CustomTabPanel value={value} index={0}>
                  <Box component="form" sx={{ '& > :not(style)': { m: 1, width: '25ch' } }} noValidate autoComplete="off">
                  </Box>
                  <div dangerouslySetInnerHTML={{ __html: rulesContent }} />
                </CustomTabPanel>
                <CustomTabPanel value={value} index={1}>
                  <Box component="form" sx={{ '& > :not(style)': { m: 1, width: '25ch' } }} noValidate autoComplete="off">
                  </Box>
                  <div dangerouslySetInnerHTML={{ __html: rules_itemContent }} />
                </CustomTabPanel>
              </Box>
            </Typography>
          </Box>
        </Modal>
      </main>
    </>
  );

}

