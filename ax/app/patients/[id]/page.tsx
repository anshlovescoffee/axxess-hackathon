"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { ArrowLeft } from "lucide-react"

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

interface Visit {
  pid: string
  nurse: string
  heart_rate: number
  reason: string
  notes: string
  respiratory_rate: number
  temperature: number
  bp_systolic: number
  bp_diastolic: number
}

interface Prescription {
  pid: string
  medication: string
  dosage: number
  unit: string
  exp_date: string
}

export default function PatientDetailsPage({ params }: { params: { id: string } }) {
  const [patient, setPatient] = useState<Patient | null>(null)
  const [visits, setVisits] = useState<Visit[]>([])
  const [prescriptions, setPrescriptions] = useState<Prescription[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchPatientData = async () => {
      try {
        // Fetch all patients and find the matching one
        const patientsResponse = await fetch('http://localhost:3000/patients1')
        const patientsText = await patientsResponse.text()
        // Split the text into lines and parse each line
        const patients = patientsText.trim().split('\n').map(line => {
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
        const foundPatient = patients.find(p => p.pid === params.id)
        if (!foundPatient) throw new Error('Patient not found')
        setPatient(foundPatient)

        // Fetch visits
        const visitsResponse = await fetch('http://localhost:3000/visits1')
        const visitsText = await visitsResponse.text()
        const allVisits = visitsText.trim().split('\n').map(line => {
          const [pid, nurse, heart_rate, reason, notes, respiratory_rate, temperature, bp_systolic, bp_diastolic] = line.split(' ')
          return {
            pid,
            nurse,
            heart_rate: parseInt(heart_rate),
            reason,
            notes,
            respiratory_rate: parseInt(respiratory_rate),
            temperature: parseInt(temperature),
            bp_systolic: parseFloat(bp_systolic),
            bp_diastolic: parseFloat(bp_diastolic)
          }
        })
        const patientVisits = allVisits.filter(visit => visit.pid === params.id)
        setVisits(patientVisits)

        // Fetch prescriptions
        const prescriptionsResponse = await fetch('http://localhost:3000/prescriptions1')
        const prescriptionsText = await prescriptionsResponse.text()
        const allPrescriptions = prescriptionsText.trim().split('\n').map(line => {
          const [pid, medication, dosage, unit, exp_date] = line.split(' ')
          return {
            pid,
            medication,
            dosage: parseInt(dosage),
            unit,
            exp_date
          }
        })
        const patientPrescriptions = allPrescriptions.filter(prescription => prescription.pid === params.id)
        setPrescriptions(patientPrescriptions)

      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch data')
      } finally {
        setIsLoading(false)
      }
    }

    if (params.id) {
      fetchPatientData()
    }
  }, [params.id])

  if (isLoading) {
    return <div className="flex items-center justify-center min-h-screen">Loading patient data...</div>
  }

  if (error || !patient) {
    return <div className="flex items-center justify-center min-h-screen text-red-500">
      Error: {error || 'Patient not found'}
    </div>
  }

  return (
    <div className="min-h-screen p-8">
      <div className="mb-6">
        <Link href="/patients" className="inline-flex items-center text-blue-600 hover:text-blue-800">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Patients
        </Link>
      </div>

      <div className="space-y-6">
        {/* Patient Information */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Patient Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p><span className="font-semibold">Name:</span> {patient.name}</p>
              <p><span className="font-semibold">DOB:</span> {new Date(patient.dob).toLocaleDateString()}</p>
              <p><span className="font-semibold">Age:</span> {patient.age}</p>
              <p><span className="font-semibold">Sex:</span> {patient.sex === 1 ? "Female" : "Male"}</p>
            </div>
            <div>
              <p><span className="font-semibold">Address:</span> {patient.address}</p>
              <p><span className="font-semibold">City:</span> {patient.city}</p>
              <p><span className="font-semibold">State:</span> {patient.state}</p>
              <p><span className="font-semibold">Phone:</span> {patient.phone}</p>
            </div>
          </div>
        </div>

        {/* Physical Information */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Physical Information</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p><span className="font-semibold">Weight:</span> {patient.weight} lbs</p>
            </div>
            <div>
              <p><span className="font-semibold">Height:</span> {patient.height} inches</p>
            </div>
          </div>
        </div>

        {/* Visits */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Visit History</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nurse</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reason</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Vitals</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Notes</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {visits.map((visit, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4">{visit.nurse}</td>
                    <td className="px-6 py-4">{visit.reason}</td>
                    <td className="px-6 py-4">
                      BP: {visit.bp_systolic}/{visit.bp_diastolic}<br />
                      HR: {visit.heart_rate} bpm<br />
                      RR: {visit.respiratory_rate} bpm<br />
                      Temp: {visit.temperature}°F
                    </td>
                    <td className="px-6 py-4">{visit.notes}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Prescriptions */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold mb-4">Prescriptions</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Medication</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Dosage</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Unit</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Expiration Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {prescriptions.map((prescription, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4">{prescription.medication}</td>
                    <td className="px-6 py-4">{prescription.dosage}</td>
                    <td className="px-6 py-4">{prescription.unit}</td>
                    <td className="px-6 py-4">{new Date(prescription.exp_date).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}