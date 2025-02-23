"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"

interface PatientData {
  PID: number
  P_Name: string
  DOB: string
  SSN: number
  Address: string
  Zipcode: number
  State_Abv: string
  phone_num: string
}

interface EditPatientModalProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (data: PatientData) => void
  patientData: PatientData | null
}

export function EditPatientModal({ isOpen, onClose, onSubmit, patientData }: EditPatientModalProps) {
  const [formData, setFormData] = useState<PatientData>({
    PID: 0,
    P_Name: "",
    DOB: "",
    SSN: 0,
    Address: "",
    Zipcode: 0,
    State_Abv: "",
    phone_num: "",
  })

  useEffect(() => {
    if (patientData) {
      setFormData(patientData)
    }
  }, [patientData])

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit(formData)
  }

  if (!patientData) {
    return null
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Edit Patient Information</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="P_Name" className="text-right">
                Name
              </Label>
              <Input
                id="P_Name"
                name="P_Name"
                value={formData.P_Name}
                onChange={handleChange}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="DOB" className="text-right">
                Date of Birth
              </Label>
              <Input
                id="DOB"
                name="DOB"
                type="date"
                value={formData.DOB}
                onChange={handleChange}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="SSN" className="text-right">
                SSN
              </Label>
              <Input
                id="SSN"
                name="SSN"
                type="number"
                value={formData.SSN}
                onChange={handleChange}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="Address" className="text-right">
                Address
              </Label>
              <Input
                id="Address"
                name="Address"
                value={formData.Address}
                onChange={handleChange}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="Zipcode" className="text-right">
                Zipcode
              </Label>
              <Input
                id="Zipcode"
                name="Zipcode"
                type="number"
                value={formData.Zipcode}
                onChange={handleChange}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="State_Abv" className="text-right">
                State
              </Label>
              <Input
                id="State_Abv"
                name="State_Abv"
                value={formData.State_Abv}
                onChange={handleChange}
                className="col-span-3"
                required
                maxLength={2}
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="phone_num" className="text-right">
                Phone
              </Label>
              <Input
                id="phone_num"
                name="phone_num"
                value={formData.phone_num}
                onChange={handleChange}
                className="col-span-3"
                required
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit">Update Patient</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

