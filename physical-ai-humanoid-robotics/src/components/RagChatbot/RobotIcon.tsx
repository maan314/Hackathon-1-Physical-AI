import React from 'react';

interface RobotIconProps {
  size?: number;
}

export default function RobotIcon({ size = 24 }: RobotIconProps): JSX.Element {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Warm gradient background circle */}
      <defs>
        <radialGradient id="bgGradient" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="#FF8C42" />
          <stop offset="100%" stopColor="#F5A623" />
        </radialGradient>
      </defs>
      <circle cx="50" cy="50" r="48" fill="url(#bgGradient)" />

      {/* Robot body - rounded rectangle */}
      <rect x="25" y="35" width="50" height="45" rx="12" fill="#00BCD4" stroke="#333" strokeWidth="1" />

      {/* Robot head - circle */}
      <circle cx="50" cy="25" r="18" fill="#4DD0E1" stroke="#333" strokeWidth="1" />

      {/* Eyes - simple circles */}
      <circle cx="43" cy="22" r="3" fill="#333" />
      <circle cx="57" cy="22" r="3" fill="#333" />

      {/* Smiling mouth */}
      <path d="M40 30 Q50 35 60 30" stroke="#333" strokeWidth="1.5" fill="none" />

      {/* Headset microphone arm */}
      <path d="M35 25 Q30 15 25 20" stroke="#333" strokeWidth="2" fill="none" />
      <circle cx="25" cy="20" r="2" fill="#333" />

      {/* Laptop base */}
      <rect x="15" y="65" width="35" height="12" rx="2" fill="#E0E0E0" stroke="#333" strokeWidth="1" />

      {/* Laptop screen */}
      <rect x="20" y="50" width="25" height="15" rx="1" fill="#B0BEC5" stroke="#333" strokeWidth="1" />

      {/* Speech bubble */}
      <path
        d="M75 25 C85 25 85 35 75 35 C70 35 70 30 75 25 Z"
        fill="#FFFFFF"
        stroke="#333"
        strokeWidth="1"
      />
      <text
        x="75"
        y="32"
        textAnchor="middle"
        fontSize="8"
        fill="#333"
        fontFamily="Arial, sans-serif"
      >
        Hi!
      </text>
    </svg>
  );
}