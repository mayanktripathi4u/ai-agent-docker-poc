import os
import sys
import hl7
from hl7apy import core
from hl7apy.parser import parse_message
from faker import Faker
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()
fake = Faker()
mcp = FastMCP("HL7-Master")

@mcp.tool()
async def generate_hl7_message(message_type: str = "ADT", trigger_event: str = "A01") -> str:
    """Generate a synthetic HL7 message with fake patient data."""
    # Initialize a basic message structure
    m = core.Message(message_type + "_" + trigger_event)
    
    # Fill MSH (Message Header)
    m.msh.msh_3 = "MCP_GEN"
    m.msh.msh_7 = fake.date_time().strftime("%Y%m%d%H%M")
    
    # Fill PID (Patient Identification)
    m.add_segment("PID")
    m.pid.pid_3 = str(fake.random_int(min=1000, max=9999))
    m.pid.pid_5 = f"{fake.last_name()}^{fake.first_name()}"
    m.pid.pid_7 = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y%m%d")
    m.pid.pid_8 = fake.random_element(elements=("M", "F", "U"))
    
    return m.to_er7().replace('\r', '\n')

@mcp.tool()
async def parse_hl7_message(raw_message: str) -> dict:
    """Parse a raw HL7 string into a JSON-friendly dictionary structure."""
    try:
        # Clean the message for the parser
        clean_msg = raw_message.strip().replace('\n', '\r')
        h = hl7.parse(clean_msg)
        
        parsed_data = {}
        for segment in h:
            seg_name = str(segment[0])
            parsed_data[seg_name] = [str(field) for field in segment]
            
        return {"status": "success", "data": parsed_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def extract_hl7_details(raw_message: str, fields: list[str]) -> dict:
    """Extract specific details like Patient Name or HL7 Version from a message."""
    try:
        clean_msg = raw_message.strip().replace('\n', '\r')
        m = parse_message(clean_msg)
        
        extracted = {}
        # Mapping common requests to HL7 attributes
        mapping = {
            "patient_name": lambda msg: str(msg.pid.pid_5),
            "hl7_version": lambda msg: str(msg.msh.msh_12),
            "facility": lambda msg: str(msg.msh.msh_4),
            "message_date": lambda msg: str(msg.msh.msh_7)
        }
        
        for field in fields:
            if field in mapping:
                extracted[field] = mapping[field](m)
                
        return extracted
    except Exception as e:
        return {"error": f"Extraction failed: {str(e)}"}

def main():
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    if transport in ["sse", "http"]:
        port = int(os.getenv("PORT", 8000))
        mcp.run(transport="sse", port=port)
    else:
        mcp.run(transport="stdio")

if __name__ == "__main__":
    main()