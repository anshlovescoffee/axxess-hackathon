"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"

interface AddPatientModalProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (data: any) => void
}

export function AddPatientModal({ isOpen, onClose, onSubmit }: AddPatientModalProps) {
  const [P_Name, setP_Name] = useState("")
  const [DOB, setDOB] = useState("")
  const [SSN, setSSN] = useState("")
  const [Address, setAddress] = useState("")
  const [Zipcode, setZipcode] = useState("")
  const [State_Abv, setState_Abv] = useState("")
  const [phone_num, setPhone_num] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      P_Name,
      DOB,
      SSN: Number.parseInt(SSN),
      Address,
      Zipcode: Number.parseInt(Zipcode),
      State_Abv,
      phone_num,
    })
    // Reset form
    setP_Name("")
    setDOB("")
    setSSN("")
    setAddress("")
    setZipcode("")
    setState_Abv("")
    setPhone_num("")
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Patient</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="P_Name" className="text-right">
                Name
              </Label>
              <Input
                id="P_Name"
                value={P_Name}
                onChange={(e) => setP_Name(e.target.value)}
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
                type="date"
                value={DOB}
                onChange={(e) => setDOB(e.target.value)}
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
                type="number"
                value={SSN}
                onChange={(e) => setSSN(e.target.value)}
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
                value={Address}
                onChange={(e) => setAddress(e.target.value)}
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
                type="number"
                value={Zipcode}
                onChange={(e) => setZipcode(e.target.value)}
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
                value={State_Abv}
                onChange={(e) => setState_Abv(e.target.value)}
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
                value={phone_num}
                onChange={(e) => setPhone_num(e.target.value)}
                className="col-span-3"
                required
                maxLength={10}
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit">Add Patient</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

