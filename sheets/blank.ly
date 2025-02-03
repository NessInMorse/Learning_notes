\version "2.24.4"

\header{
	title = ""
	composer = ""
	tagline = " "
}


\layout {
	#(layout-set-staff-size 25)
  	\context {
    	\Score
		barNumberVisibility = #first-bar-number-invisible-save-broken-bars
		\override BarNumber.break-visibility = ##(#f #t #t) 
		% barNumberVisibility = #(modulo-bar-number-visible 4 1)


		\override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1 100)
		\override MeasureSpacing.minimum-length = 50
		\override MeasureSpacing.strechtability = 1

  	}
}


\new PianoStaff \with {
}
<<

	\new Staff = "RH" {
		\time 4/4
		\key c \major
		\relative{
			NOTE_TREBLE
		}
	}

	\new Dynamics {

	}



	\new Staff = "LH" {
		\clef bass
		\set Staff.pedalSustainStyle = #'bracket
  		\set Staff.ottavationMarkups = #ottavation-ordinals
		\relative{
			NOTE_BASS
		}
	}

>> 


