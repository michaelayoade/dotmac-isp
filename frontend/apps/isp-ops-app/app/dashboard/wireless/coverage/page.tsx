'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@dotmac/ui';
import { Badge } from '@dotmac/ui';
import { Button } from '@dotmac/ui';
import { Input } from '@dotmac/ui';
import { Label } from '@dotmac/ui';
import { useRBAC } from '@/contexts/RBACContext';
import {
  useCoverageZoneListGraphQL,
  getFrequencyBandLabel,
} from '@/hooks/useWirelessGraphQL';
import { CoverageZone } from '@/lib/graphql/generated';
import { platformConfig } from '@/lib/config';
import { MapPin, Search, Filter, ChevronLeft, ChevronRight, RefreshCw, Activity, Signal } from 'lucide-react';
import Link from 'next/link';

export default function CoverageZonesPage() {
  const { hasPermission } = useRBAC();
  const hasWirelessAccess = platformConfig.features.enableNetwork && hasPermission('isp.ipam.read');

  // Filter state
  const [search, setSearch] = useState('');
  const [limit] = useState(50);
  const [offset, setOffset] = useState(0);

  // Fetch coverage zones
  const {
    zones: coverageZones,
    total: totalCount,
    hasNextPage,
    loading,
    error,
    refetch,
  } = useCoverageZoneListGraphQL({
    limit,
    offset,
    search,
    pollInterval: 60000, // Refresh every minute
  });

  if (!hasWirelessAccess) {
    return (
      <main className="max-w-7xl mx-auto px-6 py-12 space-y-8">
        <Card>
          <CardHeader>
            <CardTitle>Coverage Zones</CardTitle>
            <CardDescription>
              Access requires <code>isp.ipam.read</code> permission.
            </CardDescription>
          </CardHeader>
        </Card>
      </main>
    );
  }

  const handleNextPage = () => {
    if (hasNextPage) {
      setOffset(offset + limit);
    }
  };

  const handlePreviousPage = () => {
    if (offset > 0) {
      setOffset(Math.max(0, offset - limit));
    }
  };

  const formatType = (type: string) => {
    return type.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, (l) => l.toUpperCase());
  };

  const getSignalColor = (signalDbm: number | null | undefined) => {
    if (!signalDbm) return 'text-gray-600';
    if (signalDbm >= -50) return 'text-green-600';
    if (signalDbm >= -70) return 'text-amber-600';
    return 'text-red-600';
  };

  const getCoverageTypeColor = (type: string) => {
    switch (type) {
      case 'PRIMARY':
        return 'default';
      case 'SECONDARY':
        return 'secondary';
      case 'OVERLAP':
        return 'outline';
      default:
        return 'secondary';
    }
  };

  return (
    <main className="max-w-7xl mx-auto px-6 py-12 space-y-8">
      {/* Header */}
      <header className="flex items-center justify-between">
        <div className="space-y-1">
          <h1 className="text-2xl font-semibold text-foreground">Coverage Zones</h1>
          <p className="text-sm text-muted-foreground">
            Wireless coverage area definitions and signal strength mapping
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => refetch()}>
            <RefreshCw className="mr-2 h-4 w-4" />
            Refresh
          </Button>
          <Link href="/dashboard/wireless">
            <Button variant="outline">
              <Activity className="mr-2 h-4 w-4" />
              Back to Dashboard
            </Button>
          </Link>
        </div>
      </header>

      {/* Summary Cards */}
      {!loading && coverageZones.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Zones</CardTitle>
              <MapPin className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{totalCount}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Coverage Radius</CardTitle>
              <Signal className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {(
                  coverageZones.reduce((sum: number, zone: CoverageZone) => sum + ((zone.coverageAreaSqm ? Math.sqrt(zone.coverageAreaSqm / Math.PI) : 0) || 0), 0) /
                  coverageZones.length
                ).toFixed(0)}
                m
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Signal Strength</CardTitle>
              <Signal className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {(
                  coverageZones.reduce((sum: number, zone: CoverageZone) => sum + (zone.signalStrengthAvgDbm || 0), 0) /
                  coverageZones.filter((z: CoverageZone) => z.signalStrengthAvgDbm).length
                ).toFixed(1)}{' '}
                dBm
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Coverage Area</CardTitle>
              <MapPin className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {(
                  coverageZones.reduce(
                    (sum: number, zone: CoverageZone) =>
                      sum + ((zone.coverageAreaSqm ? Math.sqrt(zone.coverageAreaSqm / Math.PI) : 0) ? Math.PI * Math.pow((zone.coverageAreaSqm ? Math.sqrt(zone.coverageAreaSqm / Math.PI) : 0) / 1000, 2) : 0),
                    0
                  )
                ).toFixed(2)}{' '}
                km²
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filters */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Filter className="h-5 w-5" />
              <CardTitle>Filters</CardTitle>
            </div>
            <Button variant="ghost" size="sm" onClick={() => setSearch('')}>
              Clear Filters
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <Label htmlFor="search">Search</Label>
            <div className="relative">
              <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                id="search"
                placeholder="Search zones by name..."
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  setOffset(0);
                }}
                className="pl-8"
              />
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Results */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>
              Coverage Zones{' '}
              {totalCount > 0 && <span className="text-muted-foreground">({totalCount})</span>}
            </CardTitle>
            {loading && <Badge variant="outline">Loading...</Badge>}
          </div>
          {error && <p className="text-sm text-destructive">{error}</p>}
        </CardHeader>
        <CardContent>
          {coverageZones.length === 0 && !loading ? (
            <div className="text-center py-12">
              <MapPin className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
              <h3 className="text-lg font-medium mb-2">No coverage zones found</h3>
              <p className="text-sm text-muted-foreground mb-4">
                {search
                  ? 'Try adjusting your search'
                  : 'No coverage zones have been defined yet'}
              </p>
              <Button variant="outline" onClick={() => refetch()}>
                Refresh
              </Button>
            </div>
          ) : (
            <>
              {/* Grid View */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {coverageZones.map((zone: CoverageZone) => (
                  <Card key={zone.id} className="hover:border-primary/50 transition-colors">
                    <CardHeader>
                      <div className="flex items-start justify-between">
                        <div className="space-y-1 flex-1">
                          <CardTitle className="text-lg">{zone.name}</CardTitle>
                          <CardDescription>
                            Unknown Access Point
                          </CardDescription>
                        </div>
                        {zone.areaType && (
                          <Badge variant={getCoverageTypeColor(zone.areaType) as any}>
                            {formatType(zone.areaType)}
                          </Badge>
                        )}
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      {/* Location */}
                      <div className="space-y-2">
                        <div className="text-sm font-medium">Location</div>
                        <div className="font-mono text-xs text-muted-foreground">
                          Site: {zone.siteName || zone.siteId}
                        </div>
                      </div>

                      {/* Coverage Details */}
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <div className="text-muted-foreground mb-1">Coverage Radius</div>
                          <div className="font-medium">
                            {(zone.coverageAreaSqm ? Math.sqrt(zone.coverageAreaSqm / Math.PI) : 0) ? `${(zone.coverageAreaSqm ? Math.sqrt(zone.coverageAreaSqm / Math.PI) : 0).toFixed(0)}m` : '-'}
                          </div>
                        </div>
                        <div>
                          <div className="text-muted-foreground mb-1">Signal Strength</div>
                          <div className={`font-medium ${getSignalColor(zone.signalStrengthAvgDbm)}`}>
                            {zone.signalStrengthAvgDbm ? `${zone.signalStrengthAvgDbm} dBm` : '-'}
                          </div>
                        </div>
                      </div>

                      {/* Frequency Info */}
                      <div>
                        <div className="text-sm text-muted-foreground mb-1">Frequency Band</div>
                        <Badge variant="outline">
                          Mixed Bands
                        </Badge>
                      </div>

                      {/* Description */}
                      {zone.description && (
                        <div>
                          <div className="text-sm text-muted-foreground mb-1">Description</div>
                          <div className="text-sm">{zone.description}</div>
                        </div>
                      )}

                      {/* View on Map Button */}
                      <Button variant="outline" className="w-full mt-2" size="sm">
                        <MapPin className="mr-2 h-4 w-4" />
                        View on Map
                      </Button>
                    </CardContent>
                  </Card>
                ))}
              </div>

              {/* Pagination */}
              {totalCount > limit && (
                <div className="flex items-center justify-between pt-6 border-t mt-6">
                  <p className="text-sm text-muted-foreground">
                    Showing {offset + 1} to {Math.min(offset + limit, totalCount)} of{' '}
                    {totalCount} zones
                  </p>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handlePreviousPage}
                      disabled={offset === 0 || loading}
                    >
                      <ChevronLeft className="h-4 w-4 mr-1" />
                      Previous
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleNextPage}
                      disabled={!hasNextPage || loading}
                    >
                      Next
                      <ChevronRight className="h-4 w-4 ml-1" />
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {/* Coverage Map (Placeholder) */}
      <Card>
        <CardHeader>
          <CardTitle>Coverage Map</CardTitle>
          <CardDescription>Geographic visualization of wireless coverage zones</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="h-96 rounded-lg border bg-muted flex items-center justify-center">
            <div className="text-center space-y-2">
              <MapPin className="h-8 w-8 mx-auto text-muted-foreground" />
              <p className="text-sm text-muted-foreground">
                Interactive coverage map will be displayed here
              </p>
              <p className="text-xs text-muted-foreground">
                Showing {coverageZones.length} coverage zones
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </main>
  );
}
