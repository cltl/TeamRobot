/**
 * This file is part of CERMINE project.
 * Copyright (c) 2011-2016 ICM-UW
 *
 * CERMINE is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * CERMINE is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with CERMINE. If not, see <http://www.gnu.org/licenses/>.
 */

package pl.edu.icm.cermine.bibref.parsing.features;

import java.util.Arrays;
import java.util.List;
import pl.edu.icm.cermine.bibref.parsing.model.Citation;
import pl.edu.icm.cermine.bibref.parsing.model.CitationToken;
import pl.edu.icm.cermine.tools.classification.general.FeatureCalculator;

/**
 * @author Dominika Tkaczyk (d.tkaczyk@icm.edu.pl)
 */
public class IsCommonSourceWordFeature extends FeatureCalculator<CitationToken, Citation> {

    private static final List<String> KEYWORDS = Arrays.asList(
            "acad", "acta", "algebra", "amer", "anal", "ann", "annales", "annals", "appl",
            "bourbaki", "bull",
            "comm", "comptes",
            "fields", "fourier",
            "geom",
            "inst", "invent",
            "journal",
            "lett",
            "mat", "math", "mathematical", "mathematics",
            "phys", "physics", "probab", "proc", "publ", "pure",
            "séminaire", "sc", "sci", "sciences", "soc", "studies",
            "theory", "trans",
            "univ"
            );

    @Override
    public double calculateFeatureValue(CitationToken object, Citation context) {
        return (KEYWORDS.contains(object.getText().toLowerCase())) ? 1 : 0;
    }
}
