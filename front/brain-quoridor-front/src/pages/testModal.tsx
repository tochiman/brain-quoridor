// src/pages/testModal.tsx

import React, { useState } from 'react';
import Button from '@mui/material/Button';
import SettingModal from '../components/settingModal';

export default function TestModal() {
  const [open, setOpen] = useState(false);

  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  return (
    <div>
      <Button variant="contained" onClick={handleOpen}>
        設定を開く
      </Button>
      <SettingModal open={open} handleClose={handleClose} />
    </div>
  );
}
