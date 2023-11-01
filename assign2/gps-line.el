(defun gps-line ()
  "Print the current line number out of the total number of lines in the buffer."
  (interactive)
  (save-restriction
    (widen)
    (save-excursion
      (beginning-of-line)
      (let ((current-line (1+ (count-lines 1 (point))))
	    (total-lines (count-matches "\n" (point-min) (point-max))))
	(message "Line %d/%d" current-line total-lines)))))
