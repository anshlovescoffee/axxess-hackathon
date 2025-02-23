"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog"

interface NewVisitationModalProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (data: any) => void
}

export function NewVisitationModal({ isOpen, onClose, onSubmit }: NewVisitationModalProps) {
  const [N_Name, setN_Name] = useState("")
  const [Date_of_visitation, setDate_of_visitation] = useState("")
  const [Notes, setNotes] = useState("")
  const [Respiratory_Rate, setRespiratory_Rate] = useState("")
  const [Heart_Rate, setHeart_Rate] = useState("")
  const [bp_systolic, setBp_systolic] = useState("")
  const [bp_diastolic, setBp_diastolic] = useState("")
  const [Temp, setTemp] = useState("")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSubmit({
      N_Name,
      Date_of_visitation,
      Notes,
      Respiratory_Rate: Number.parseInt(Respiratory_Rate),
      Heart_Rate: Number.parseInt(Heart_Rate),
      bp_systolic: Number.parseInt(bp_systolic),
      bp_diastolic: Number.parseInt(bp_diastolic),
      Temp: Number.parseInt(Temp),
    })
    // Reset form
    setN_Name("")
    setDate_of_visitation("")
    setNotes("")
    setRespiratory_Rate("")
    setHeart_Rate("")
    setBp_systolic("")
    setBp_diastolic("")
    setTemp("")
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Add New Visitation</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="N_Name" className="text-right">
                Doctor/Nurse
              </Label>
              <Input
                id="N_Name"
                value={N_Name}
                onChange={(e) => setN_Name(e.target.value)}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="Date_of_visitation" className="text-right">
                Date
              </Label>
              <Input
                id="Date_of_visitation"
                type="date"
                value={Date_of_visitation}
                onChange={(e) => setDate_of_visitation(e.target.value)}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="Respiratory_Rate" className="text-right">
                Respiratory Rate
              </Label>
              <Input
                id="Respiratory_Rate"
                type="number"
                value={Respiratory_Rate}
                onChange={(e) => setRespiratory_Rate(e.target.value)}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="Heart_Rate" className="text-right">
                Heart Rate
              </Label>
              <Input
                id="Heart_Rate"
                type="number"
                value={Heart_Rate}
                onChange={(e) => setHeart_Rate(e.target.value)}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="bp_systolic" className="text-right">
                BP Systolic
              </Label>
              <Input
                id="bp_systolic"
                type="number"
                value={bp_systolic}
                onChange={(e) => setBp_systolic(e.target.value)}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="bp_diastolic" className="text-right">
                BP Diastolic
              </Label>
              <Input
                id="bp_diastolic"
                type="number"
                value={bp_diastolic}
                onChange={(e) => setBp_diastolic(e.target.value)}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="Temp" className="text-right">
                Temperature
              </Label>
              <Input
                id="Temp"
                type="number"
                value={Temp}
                onChange={(e) => setTemp(e.target.value)}
                className="col-span-3"
                required
              />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="Notes" className="text-right">
                Notes
              </Label>
              <Textarea id="Notes" value={Notes} onChange={(e) => setNotes(e.target.value)} className="col-span-3" />
            </div>
          </div>
          <DialogFooter>
            <Button type="submit">Add Visitation</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

