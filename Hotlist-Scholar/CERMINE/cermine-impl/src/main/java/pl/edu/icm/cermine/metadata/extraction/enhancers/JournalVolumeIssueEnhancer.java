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

package pl.edu.icm.cermine.metadata.extraction.enhancers;

import com.google.common.collect.Lists;
import java.util.EnumSet;
import java.util.List;
import java.util.Set;
import java.util.regex.MatchResult;
import java.util.regex.Pattern;
import pl.edu.icm.cermine.metadata.model.DocumentMetadata;
import pl.edu.icm.cermine.structure.model.BxZoneLabel;
import pl.edu.icm.cermine.tools.CharacterUtils;

/**
 * @author Dominika Tkaczyk (d.tkaczyk@icm.edu.pl)
 */
public class JournalVolumeIssueEnhancer extends AbstractMultiPatternEnhancer {

    private static final List<Pattern> PATTERNS = Lists.newArrayList(
            Pattern.compile("([A-Z][^0-9]*) (\\d{1,3})[,: ]+(\\d+)(?=[^\\d" + String.valueOf(CharacterUtils.DASH_CHARS) + "]|$)"),
            Pattern.compile("([A-Z][^0-9]*).*[^0-9](\\d{1,3})[,: ]*\\((\\d+)\\)")
            );
    
    private static final Set<BxZoneLabel> SEARCHED_ZONE_LABELS = EnumSet.of(BxZoneLabel.MET_BIB_INFO);

    public JournalVolumeIssueEnhancer() {
        super(PATTERNS, SEARCHED_ZONE_LABELS);
    }
    
    @Override
    protected Set<EnhancedField> getEnhancedFields() {
        return EnumSet.of(EnhancedField.JOURNAL, EnhancedField.VOLUME, EnhancedField.ISSUE);
    }

    @Override
    protected boolean enhanceMetadata(MatchResult result, DocumentMetadata metadata) {
        metadata.setJournal(result.group(1).trim()
                .replaceAll("Published as: ", "").replaceAll(",$", "")
                .replaceAll(".*/", "").trim());
        metadata.setVolume(result.group(2));
        metadata.setIssue(result.group(3));
       
        return true;
    }
}
