from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime
import uuid

from src.models.hardware import HardwareComponent, HardwareSetup, HardwareLab, HardwareRecommendation
from src.database.database import get_db


class HardwareService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_hardware_components(self) -> List[HardwareComponent]:
        """
        Get all hardware components for the textbook
        """
        # In a real implementation, this would fetch from the database
        # For now, we'll return predefined hardware components
        components = [
            HardwareComponent(
                id="comp-1",
                name="NVIDIA Jetson AGX Orin",
                description="AI supercomputer for autonomous machines",
                category="processors",
                manufacturer="NVIDIA",
                model="Jetson AGX Orin",
                specifications={
                    "cpu": "12-core ARM Cortex-A78AE v8.2 64-bit",
                    "gpu": "NVIDIA Ampere architecture with 2048 CUDA cores",
                    "memory": "32GB 256-bit LPDDR5",
                    "ai_performance": "275 TOPS (int8)"
                },
                price=599.00,
                availability="both",
                sim_to_real_latency=10.0,
                sim_to_real_accuracy=0.95
            ),
            HardwareComponent(
                id="comp-2",
                name="LDS-01 Laser Distance Sensor",
                description="2D LIDAR sensor for navigation and mapping",
                category="sensors",
                manufacturer="Hokuyo",
                model="URG-04LX-UG01",
                specifications={
                    "range": "0.06m to 5.6m",
                    "angle": "240 degrees",
                    "accuracy": "±30mm",
                    "scan_time": "0.1 sec"
                },
                price=450.00,
                availability="both",
                sim_to_real_latency=5.0,
                sim_to_real_accuracy=0.98
            ),
            HardwareComponent(
                id="comp-3",
                name="Dynamixel MX-28 Servo",
                description="High-performance servo for humanoid joints",
                category="actuators",
                manufacturer="Robotis",
                model="MX-28",
                specifications={
                    "torque": "2.5 N·m at 12V",
                    "speed": "55 RPM at 12V",
                    "resolution": "0.344 degree",
                    "communication": "RS-485"
                },
                price=120.00,
                availability="both",
                sim_to_real_latency=2.0,
                sim_to_real_accuracy=0.92
            )
        ]
        return components

    async def get_hardware_setups(self) -> List[HardwareSetup]:
        """
        Get all hardware setups for different lab paths
        """
        setups = [
            HardwareSetup(
                id="setup-1",
                name="Cloud-Based Humanoid Lab",
                description="Complete humanoid robotics lab using cloud simulation",
                components=["comp-1", "comp-2", "comp-3"],
                difficulty_level="intermediate",
                estimated_cost=1169.00,
                estimated_time="1-2 weeks",
                lab_path="cloud",
                sim_to_real_considerations=[
                    "Higher latency when connecting to physical hardware",
                    "Need for stable internet connection",
                    "Cloud simulation accuracy may vary"
                ]
            ),
            HardwareSetup(
                id="setup-2",
                name="On-Prem Humanoid Lab",
                description="Complete humanoid robotics lab with local simulation",
                components=["comp-1", "comp-2", "comp-3"],
                difficulty_level="advanced",
                estimated_cost=1169.00,
                estimated_time="2-4 weeks",
                lab_path="on-prem",
                sim_to_real_considerations=[
                    "Lower latency for real-time control",
                    "Higher computational requirements",
                    "More complex setup and maintenance"
                ]
            )
        ]
        return setups

    async def get_hardware_labs(self) -> List[HardwareLab]:
        """
        Get all hardware labs with cloud vs on-prem comparisons
        """
        labs = [
            HardwareLab(
                id="lab-1",
                name="Humanoid Navigation Lab",
                description="Implement navigation algorithms on a humanoid robot",
                setup_id="setup-1",
                requirements=[
                    "NVIDIA Jetson AGX Orin",
                    "LDS-01 Laser Distance Sensor",
                    "Dynamixel MX-28 Servos (20 units)"
                ],
                safety_considerations=[
                    "Ensure safe operating area",
                    "Implement emergency stop mechanisms",
                    "Monitor robot behavior at all times"
                ],
                cloud_vs_on_prem_comparison={
                    "latency": {"cloud": "50-100ms", "on_prem": "5-10ms"},
                    "cost": {"cloud": "$200/month", "on_prem": "$1200 one-time"},
                    "setup_time": {"cloud": "1 day", "on_prem": "1 week"},
                    "maintenance": {"cloud": "Minimal", "on_prem": "High"}
                },
                latency_warnings=[
                    "High latency (>50ms) can cause instability in real-time control",
                    "Network jitter can affect sensor data accuracy"
                ],
                sim_to_real_warnings=[
                    "Simulation physics may not perfectly match real-world behavior",
                    "Motor dynamics in simulation may differ from physical motors"
                ],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            HardwareLab(
                id="lab-2",
                name="Humanoid Manipulation Lab",
                description="Implement manipulation algorithms on a humanoid robot",
                setup_id="setup-2",
                requirements=[
                    "NVIDIA Jetson AGX Orin",
                    "RGB-D Camera",
                    "Dynamixel MX-28 Servos (24 units)"
                ],
                safety_considerations=[
                    "Ensure workspace is clear of obstacles",
                    "Implement force limiting on actuators",
                    "Use safety barriers when necessary"
                ],
                cloud_vs_on_prem_comparison={
                    "latency": {"cloud": "60-120ms", "on_prem": "10-15ms"},
                    "cost": {"cloud": "$300/month", "on_prem": "$1500 one-time"},
                    "setup_time": {"cloud": "2 days", "on_prem": "2 weeks"},
                    "maintenance": {"cloud": "Minimal", "on_prem": "High"}
                },
                latency_warnings=[
                    "Manipulation tasks require low latency (<20ms) for stability",
                    "High latency can cause jerky movements and potential damage"
                ],
                sim_to_real_warnings=[
                    "Contact physics in simulation may not match real-world",
                    "Object friction and compliance models may differ significantly"
                ],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        return labs

    async def get_hardware_recommendations(self, user_experience: str) -> List[HardwareRecommendation]:
        """
        Get hardware recommendations based on user experience
        """
        recommendations = []

        if user_experience in ["beginner", "intermediate"]:
            recommendations.append(
                HardwareRecommendation(
                    id="rec-1",
                    component_id="comp-1",
                    use_case="AI processing for humanoid control",
                    recommendation_type="essential",
                    justification="Required for running AI models on the robot",
                    alternative_options=["NVIDIA Jetson Nano", "Raspberry Pi 4"],
                    created_at=datetime.utcnow()
                )
            )
            recommendations.append(
                HardwareRecommendation(
                    id="rec-2",
                    component_id="comp-2",
                    use_case="Navigation and mapping",
                    recommendation_type="recommended",
                    justification="Helps with autonomous navigation capabilities",
                    alternative_options=["Stereo Camera", "Ultrasonic Sensors"],
                    created_at=datetime.utcnow()
                )
            )
        else:  # advanced user
            recommendations.append(
                HardwareRecommendation(
                    id="rec-3",
                    component_id="comp-3",
                    use_case="Humanoid joint control",
                    recommendation_type="essential",
                    justification="Core component for humanoid robot movement",
                    alternative_options=["AX-12 Servos", "Custom Actuators"],
                    created_at=datetime.utcnow()
                )
            )

        return recommendations

    async def get_cloud_vs_on_prem_comparison(self) -> dict:
        """
        Get comprehensive comparison between cloud and on-prem solutions
        """
        return {
            "performance": {
                "cloud": {
                    "latency": "50-100ms average",
                    "throughput": "Depends on internet connection",
                    "reliability": "99.9% uptime (provider dependent)"
                },
                "on_prem": {
                    "latency": "5-15ms average",
                    "throughput": "Limited by local hardware",
                    "reliability": "Depends on local setup"
                }
            },
            "cost": {
                "cloud": {
                    "initial": "$0-$500",
                    "monthly": "$100-$500",
                    "scaling": "Pay-as-you-go"
                },
                "on_prem": {
                    "initial": "$1000-$5000",
                    "monthly": "$20-$100 (electricity/maintenance)",
                    "scaling": "Capital expense"
                }
            },
            "sim_to_real_considerations": {
                "cloud": [
                    "Higher network latency affects real-time control",
                    "Bandwidth limitations may affect sensor data transfer",
                    "Internet reliability affects consistency"
                ],
                "on_prem": [
                    "Lower latency enables better real-time control",
                    "No network dependency for local operations",
                    "Higher initial investment in hardware"
                ]
            }
        }

    async def get_latency_considerations(self) -> List[dict]:
        """
        Get information about latency considerations for sim-to-real transfer
        """
        return [
            {
                "threshold": "< 10ms",
                "application": "High-frequency control loops",
                "risk": "Instability and oscillation",
                "mitigation": "Use local processing and high-speed communication"
            },
            {
                "threshold": "10-50ms",
                "application": "Standard control and planning",
                "risk": "Reduced responsiveness",
                "mitigation": "Predictive control and buffering"
            },
            {
                "threshold": "> 50ms",
                "application": "High-level decision making",
                "risk": "Poor user experience",
                "mitigation": "Offload to cloud for non-critical tasks"
            }
        ]

    async def get_sim_to_real_warnings(self) -> List[dict]:
        """
        Get warnings about sim-to-real transfer challenges
        """
        return [
            {
                "category": "Physics Simulation",
                "warning": "Simulated physics may not perfectly match real-world behavior",
                "impact": "Controllers trained in simulation may fail on real hardware",
                "solution": "Use domain randomization and system identification"
            },
            {
                "category": "Sensor Noise",
                "warning": "Simulated sensors are often idealized compared to real sensors",
                "impact": "Algorithms may be sensitive to real-world noise",
                "solution": "Add realistic noise models to simulation"
            },
            {
                "category": "Actuator Dynamics",
                "warning": "Motor response and compliance may differ between sim and reality",
                "impact": "Control commands may cause unexpected behavior",
                "solution": "Characterize real actuators and tune simulation parameters"
            }
        ]