"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { MainNav } from "@/components/main-nav"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Plus, Search } from "lucide-react"
import { AddPatientModal } from "@/components/add-patient-modal"

interface Patient {
  pid: string
  ssn: string
  name: string
  address: string
  zip: string
  age: number
  sex: number
  weight: number
  height: number
  phone: string
  dob: string
  city: string
  state: string
}

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [isAddPatientModalOpen, setIsAddPatientModalOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState("")
  const [filteredPatients, setFilteredPatients] = useState<Patient[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPatients = async () => {
      try {
        const response = await fetch('http://localhost:3000/patients1')
        const text = await response.text()
        
        // Split the text into lines and parse each line
        const patientsList = text.trim().split('\n').map(line => {
          const [pid, ssn, name, address, zip, age, sex, weight, height, phone, dob, city, state] = line.split(' ')
          return {
            pid, ssn, name, address, zip,
            age: parseInt(age),
            sex: parseInt(sex),
            weight: parseInt(weight),
            height: parseInt(height),
            phone, dob, city, state
          }
        })
        
        setPatients(patientsList)
        setFilteredPatients(patientsList)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch patients')
      } finally {
        setIsLoading(false)
      }
    }

    fetchPatients()
  }, [])

  useEffect(() => {
    const lowercasedQuery = searchQuery.toLowerCase()
    const filtered = patients.filter(
      (patient) =>
        patient.name.toLowerCase().includes(lowercasedQuery) ||
        patient.pid.toString().includes(lowercasedQuery) ||
        patient.phone.includes(lowercasedQuery)
    )
    setFilteredPatients(filtered)
  }, [patients, searchQuery])

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading patients...</div>
  }

  if (error) {
    return <div className="flex items-center justify-center min-h-screen text-red-500">Error: {error}</div>
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-14 items-center">
          <MainNav />
        </div>
      </header>
      <main className="flex-1 space-y-4 p-8 pt-6">
        <div className="flex items-center justify-between">
          <h2 className="text-3xl font-bold tracking-tight">Patient List</h2>
          <Button onClick={() => setIsAddPatientModalOpen(true)}>
            <Plus className="mr-2 h-4 w-4" />
            Add New Patient
          </Button>
        </div>
        <div className="flex items-center space-x-2">
          <div className="relative flex-1">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search patients..."
              className="pl-8"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <Button variant="outline">Filter</Button>
        </div>
        <Card>
          <CardHeader>
            <CardTitle>All Patients</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>PID</TableHead>
                  <TableHead>Name</TableHead>
                  <TableHead>Date of Birth</TableHead>
                  <TableHead>Address</TableHead>
                  <TableHead>Phone</TableHead>
                  <TableHead>State</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredPatients.map((patient) => (
                  <TableRow key={patient.pid} className="cursor-pointer hover:bg-muted/50">
                    <TableCell>{patient.pid}</TableCell>
                    <TableCell>
                      <Link href={`/patients/${patient.pid}`} className="hover:underline">
                        {patient.name}
                      </Link>
                    </TableCell>
                    <TableCell>{new Date(patient.dob).toLocaleDateString()}</TableCell>
                    <TableCell>{patient.address}</TableCell>
                    <TableCell>{patient.phone}</TableCell>
                    <TableCell>{patient.state}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </main>
      <AddPatientModal
        isOpen={isAddPatientModalOpen}
        onClose={() => setIsAddPatientModalOpen(false)}
        onSubmit={async (newPatient) => {
          // Here you would typically make an API call to add the patient
          console.log('Adding new patient:', newPatient);
          setIsAddPatientModalOpen(false);
        }}
      />
    </div>
  )
}