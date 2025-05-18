// src/pages/Dashboard.tsx

import React, { useEffect, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'      // ← runtime import
import walletService from '../services/wallet.service'
import type { Wallet, Transaction } from '../types'     // ← type-only import

import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  CircularProgress,
} from '@mui/material'
import { useNavigate } from 'react-router-dom'

const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()

  const [wallet, setWallet] = useState<Wallet | null>(null)
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [walletData, transactionsData] = await Promise.all([
          walletService.getWallet(),
          walletService.getTransactions(),    // ← renamed to match service
        ])
        setWallet(walletData)
        setTransactions(transactionsData)
      } catch (err) {
        console.error(err)
        setError('Failed to load wallet data')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
      >
        <CircularProgress />
      </Box>
    )
  }

  if (error) {
    return (
      <Container>
        <Typography color="error" align="center">
          {error}
        </Typography>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Wallet Balance Card */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Wallet Balance
            </Typography>
            <Typography component="p" variant="h4">
              {wallet?.balance.toFixed(2)} {wallet?.currency}
            </Typography>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button variant="contained" onClick={() => navigate('/deposit')}>
                Deposit
              </Button>
              <Button variant="contained" onClick={() => navigate('/withdraw')}>
                Withdraw
              </Button>
              <Button variant="contained" onClick={() => navigate('/transfer')}>
                Transfer
              </Button>
            </Box>
          </Paper>
        </Grid>

        {/* Recent Transactions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Recent Transactions
            </Typography>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Date</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Amount</TableCell>
                    <TableCell>Status</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {transactions.map((tx) => (
                    <TableRow key={tx.id}>
                      <TableCell>
                        {new Date(tx.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell>{tx.transaction_type}</TableCell>
                      <TableCell>
                        {tx.amount.toFixed(2)} {tx.currency}
                      </TableCell>
                      <TableCell>{tx.status}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  )
}

export default Dashboard
