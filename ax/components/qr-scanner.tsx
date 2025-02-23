"use client"

import { useEffect } from "react"
import { Html5QrcodeScanner } from "html5-qrcode"

interface QrScannerProps {
  onScan: (result: string) => void
  onError: (error: any) => void
}

export function QrScanner({ onScan, onError }: QrScannerProps) {
  useEffect(() => {
    const scanner = new Html5QrcodeScanner("qr-reader", { fps: 10, qrbox: 250 }, /* verbose= */ false)

    scanner.render(onScan, onError)

    return () => {
      scanner.clear().catch(console.error)
    }
  }, [onScan, onError])

  return <div id="qr-reader" style={{ width: "100%" }} />
}

