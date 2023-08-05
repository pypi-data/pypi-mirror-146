/////////////////////////////////////////////////////////////////////
////                                                             ////
////  Memory Buffer Arbiter                                      ////
////  Arbitrates between the internal DMA and external bus       ////
////  interface for the internal buffer memory                   ////
////                                                             ////
////  Author: Rudolf Usselmann                                   ////
////          rudi@asics.ws                                      ////
////                                                             ////
////                                                             ////
////  Downloaded from: http://www.opencores.org/cores/usb/       ////
////                                                             ////
/////////////////////////////////////////////////////////////////////
////                                                             ////
//// Copyright (C) 2000 Rudolf Usselmann                         ////
////                    rudi@asics.ws                            ////
////                                                             ////
//// This source file may be used and distributed without        ////
//// restriction provided that this copyright statement is not   ////
//// removed from the file and that any derivative work contains ////
//// the original copyright notice and the associated disclaimer.////
////                                                             ////
////     THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY     ////
//// EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED   ////
//// TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS   ////
//// FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL THE AUTHOR      ////
//// OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,         ////
//// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES    ////
//// (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE   ////
//// GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR        ////
//// BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF  ////
//// LIABILITY, WHETHER IN  CONTRACT, STRICT LIABILITY, OR TORT  ////
//// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT  ////
//// OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE         ////
//// POSSIBILITY OF SUCH DAMAGE.                                 ////
////                                                             ////
/////////////////////////////////////////////////////////////////////

//  CVS Log
//
//  $Id: mem_arb.v,v 1.0 2001/03/07 09:17:12 rudi Exp $
//
//  $Date: 2001/03/07 09:17:12 $
//  $Revision: 1.0 $
//  $Author: rudi $
//  $Locker:  $
//  $State: Exp $
//
// Change History:
//               $Log: mem_arb.v,v $
//               Revision 1.0  2001/03/07 09:17:12  rudi
//
//
//               Changed all revisions to revision 1.0. This is because OpenCores CVS
//               interface could not handle the original '0.1' revision ....
//
//               Revision 0.1.0.1  2001/02/28 08:10:52  rudi
//               Initial Release
//
//

`include "usb_defines.v"

module mem_arb(	phy_clk, wclk, rst,

		// SSRAM Interface
		radr, rdin, rdout, rre, rwe,

		// IDMA Memory Interface
		madr, mdout, mdin, mwe, mreq, mack,

		// WISHBONE Memory Interface
		wadr, wdout, wdin, wwe, wreq, wack

		);

input		phy_clk, wclk, rst;

output	[14:0]	radr;
input	[31:0]	rdin;
output	[31:0]	rdout;
output		rre, rwe;

input	[14:0]	madr;
output	[31:0]	mdout;
input	[31:0]	mdin;
input		mwe;
input		mreq;
output		mack;

input	[14:0]	wadr;
output	[31:0]	wdout;
input	[31:0]	wdin;
input		wwe;
input		wreq;
output		wack;

///////////////////////////////////////////////////////////////////
//
// Local Wires and Registers
//

wire		wsel;
reg	[14:0]	radr;
reg	[31:0]	rdout;
reg		rwe;
reg		mack;
reg		mack_r;
wire		mcyc;
reg		wack;
wire		wcyc;
reg		wwe_r;

///////////////////////////////////////////////////////////////////
//
// Memory Arbiter Logic
//

// IDMA has always first priority

// -----------------------------------------
// Ctrl Signals

assign wsel = (wreq | wcyc) & !mreq;

// -----------------------------------------
// SSRAM Specific
// Data Path
always @(wsel or wdin or mdin)
	if(wsel)	rdout = wdin;
	else		rdout = mdin;

// Address Path
always @(wsel or wadr or madr)
	if(wsel)	radr = wadr;
	else		radr = madr;

// Write Enable Path
always @(wsel or wwe_r or mwe or mcyc or wcyc)
	if(wsel)	rwe = wwe_r & wcyc;
	else		rwe = mwe & mcyc;

assign rre = 1;

// -----------------------------------------
// IDMA specific
assign mdout = rdin;

always @(mreq)
	mack = mreq;

always @(posedge phy_clk)
	mack_r <= #1 mack;

assign mcyc = mack;	// Qualifier for writes

// -----------------------------------------
// WISHBONE specific
assign wdout = rdin;

reg	wack_d, wack_r;

always @(wack_d or mreq)
	wack = wack_d & !mreq;

always @(posedge phy_clk)
	wack_r <= #1 wack_d;

always @(wreq or mreq)
	if(!mreq)	wack_d = wreq;
	else		wack_d = 0;

always @(posedge phy_clk)
	wwe_r <= #1 wwe;

assign wcyc = wack_d | wack_r;	// Qualifier for writes

endmodule

